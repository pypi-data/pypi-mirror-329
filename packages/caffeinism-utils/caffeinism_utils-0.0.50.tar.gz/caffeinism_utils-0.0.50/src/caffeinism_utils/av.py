import fractions
from abc import ABC, abstractmethod
from collections import deque
from concurrent.futures import ThreadPoolExecutor

import av
import av.container
import numpy as np
from pydub import AudioSegment

TIME_BASE = fractions.Fraction(1, 90000)


class PyAVInterface(ABC):
    container: av.container.Container

    @property
    def fps(self):
        return self.streams[0].base_rate or self.streams[0].codec_context.framerate

    @property
    def width(self):
        return self.streams[0].codec_context.width

    @property
    def height(self):
        return self.streams[0].codec_context.height

    @property
    def pix_fmt(self):
        return self.streams[0].format.name

    def __enter__(self):
        self.container.__enter__()
        return self

    def __exit__(self, *args):
        self.container.__exit__(*args)


class BasePyAVReader(PyAVInterface):
    def __init__(self, path):
        self.container = av.open(path, "r")

        self.streams = self.container.streams.video

        self.codec_contexts = {}
        for stream in self.streams:
            if stream.codec_context.name in ("vp8", "vp9"):
                if stream.codec_context.name == "vp8":
                    codec_name = "libvpx"
                elif stream.codec_context.name == "vp9":
                    codec_name = "libvpx-vp9"
                codec = av.codec.Codec(codec_name, "r")
                self.codec_contexts[stream] = codec.create()
            else:
                self.codec_contexts[stream] = stream.codec_context

    @abstractmethod
    def __iter__(self):
        raise NotImplementedError


class PyAVReader(BasePyAVReader):
    def __init__(self, path, start=0, end=(2 << 62) - 1):
        super().__init__(path)
        self.start = start
        self.end = end

        if len(self.streams) == 1:
            self.alpha_merger = NotAlphaMerger(self.streams[0])
        elif len(self.streams) == 2:
            self.alpha_merger = AlphaMerger(*self.streams)
        else:
            raise NotImplementedError

    def __iter__(self):
        with self:
            for packet in self.container.demux(self.streams):
                for frame in self.codec_contexts[packet.stream].decode(packet):
                    if (
                        self.start
                        <= round(frame.pts * self.fps * frame.time_base)
                        < self.end
                    ):
                        if packet.stream is self.streams[0]:
                            self.alpha_merger.push_image(frame)
                        else:
                            self.alpha_merger.push_alpha(frame)

                while (result := self.alpha_merger.pull()) is not None:
                    yield result


PyAVDisposableReader = PyAVReader


def create_stream(
    container,
    codec_name: str,
    rate: int | fractions.Fraction,
    width: int,
    height: int,
    pix_fmt: str,
    bit_rate: int,
    time_base: fractions.Fraction,
    options: dict,
):
    stream = container.add_stream(codec_name=codec_name, rate=rate)
    stream.width = width
    stream.height = height
    stream.pix_fmt = pix_fmt
    stream.bit_rate = bit_rate
    stream.time_base = time_base
    stream.options = options
    return stream


class PyAVWriter(PyAVInterface):
    def __init__(
        self,
        path,
        width: int,
        height: int,
        fps: fractions.Fraction,
        *,
        codec_name="libvpx-vp9",
        pix_fmt="yuva420p",
        bit_rate=1024 * 1024,
        alpha_stream: bool | str = False,
        audio_codec_name=None,
        format=None,
        options={},
    ):
        if pix_fmt == "yuv420p" and alpha_stream:
            pix_fmt = "yuva420p"
            alpha_stream = False

        if pix_fmt.startswith("yuva") and alpha_stream:
            alpha_stream = False

        self.container = av.open(path, "w", format=format, options=options)
        self.streams = []

        pix_fmts = [pix_fmt]
        if alpha_stream:
            pix_fmts.append(pix_fmt if alpha_stream == True else alpha_stream)

        for pf in pix_fmts:
            stream = create_stream(
                self.container,
                codec_name=codec_name,
                rate=fps,
                width=width,
                height=height,
                pix_fmt=pf,
                bit_rate=bit_rate,
                time_base=TIME_BASE,
                options=options,
            )
            self.streams.append(stream)

        self.__frames = 0

        self.alpha_extractor = AlphaExtractor(width, height) if alpha_stream else None

        self.audio_stream = None
        if audio_codec_name is not None:
            audio_stream = self.container.add_stream(
                codec_name=audio_codec_name, rate=48000
            )
            audio_stream.format = "s16"
            audio_stream.layout = "stereo"
            self.audio_stream = audio_stream

        self.pool = None
        self.future = None

    def array_to_frame(self, array):
        if self.streams[0].pix_fmt.startswith("yuva") or len(self.streams) == 2:
            frame = av.VideoFrame.from_ndarray(array, format="rgba")
        else:
            frame = av.VideoFrame.from_ndarray(array[..., :3], format="rgb24")
        return frame

    def write(self, array):
        frame = self.array_to_frame(array)
        self.write_video_frame(frame)

    def write_lazy(self, array):
        frame = self.array_to_frame(array)
        self.write_video_frame_lazy(frame)

    def write_video_frame(self, frame: av.VideoFrame):
        frames = [frame]
        if self.alpha_extractor is not None:
            frames.append(self.alpha_extractor(frame))

        for stream, frame in zip(self.streams, frames):
            frame.time_base = TIME_BASE
            frame.pts = round(self.__frames / self.fps / TIME_BASE)
            self.container.mux(stream.encode(frame))

        self.__frames += 1

    def write_video_frame_lazy(self, frame: av.VideoFrame):
        if self.pool is None:
            self.pool = ThreadPoolExecutor(1)

        if self.future is not None:
            self.future.result()
            del self.future

        self.future = self.pool.submit(self.write_video_frame, frame)

    def write_audio(self, audio_segment: AudioSegment):
        audio_segment = (
            audio_segment.set_channels(2).set_sample_width(2).set_frame_rate(48000)
        )
        audio_frame = av.AudioFrame.from_ndarray(
            np.array(audio_segment.get_array_of_samples()).reshape(1, -1)
        )
        audio_frame.sample_rate = 48000
        self.container.mux(self.audio_stream.encode(audio_frame))

    def write_audio_lazy(self, audio_segment: AudioSegment):
        if self.pool is None:
            self.pool = ThreadPoolExecutor(1)

        if self.future is not None:
            self.future.result()
            del self.future

        self.future = self.pool.submit(self.write_audio, audio_segment)

    def flush(self):
        if self.future is not None:
            self.future.result()
            del self.future

        for stream in self.streams:
            self.container.mux(stream.encode())
        if self.audio_stream is not None:
            self.container.mux(self.audio_stream.encode())

    def __exit__(self, *args):
        self.flush()
        super().__exit__(*args)


class _Formatter:
    def __init__(self, width: int, height: int, from_pix_fmt: str, to_pix_format: str):
        graph = av.filter.Graph()
        src = graph.add_buffer(
            width=width,
            height=height,
            format=from_pix_fmt,
            time_base=fractions.Fraction(1, 1000),
        )

        reformat = graph.add("format", to_pix_format)
        src.link_to(reformat)

        sink = graph.add("buffersink")
        reformat.link_to(sink)

        graph.configure()

        self.graph = graph

    def __call__(self, frame: av.VideoFrame) -> av.VideoFrame:
        self.graph.push(frame)
        ret = self.graph.pull()
        ret.pts = None
        return ret


def to_rgba(reader: BasePyAVReader):
    formatter = {}

    for frame in reader:
        if frame.format.name not in formatter:
            formatter[frame.format.name] = _Formatter(
                reader.width, reader.height, frame.format.name, "rgba"
            )

        yield formatter[frame.format.name](frame)


def to_array(iterator: list[av.VideoFrame]):
    for frame in iterator:
        yield frame.to_ndarray()


class _AlphaExtractor:
    def __init__(self, width: int, height: int, pix_fmt: str):
        graph = av.filter.Graph()
        src = graph.add_buffer(
            width=width,
            height=height,
            format=pix_fmt,
            time_base=fractions.Fraction(1, 1000),
        )

        alphaextract = graph.add("alphaextract")
        src.link_to(alphaextract)

        alpha = graph.add("buffersink")
        alphaextract.link_to(alpha)

        graph.configure()

        self.graph = graph

    def __call__(self, frame: av.VideoFrame):
        self.graph.push(frame)
        return self.graph.pull()


class AlphaExtractor:
    def __init__(self, width: int, height: int):
        assert height % 2 == 0

        self.rgba = _AlphaExtractor(width, height, "rgba")
        self.yuva420p = _AlphaExtractor(width, height, "yuva420p")

    def __call__(self, frame: av.VideoFrame):
        if frame.format.name == "rgba":
            return self.rgba(frame)
        elif frame.format.name == "yuva420p":
            return self.yuva420p(frame)
        else:
            raise NotImplementedError


class AlphaMerger:
    def __init__(self, template1: av.VideoStream, template2: av.VideoStream):
        graph = av.filter.Graph()
        self.image = graph.add_buffer(template=template1)
        self.alpha = graph.add_buffer(template=template2)
        format = graph.add("format", "gray")
        self.alpha.link_to(format)

        alphamerge = graph.add("alphamerge")
        self.image.link_to(alphamerge, input_idx=0)
        format.link_to(alphamerge, input_idx=1)

        self.result = graph.add("buffersink")
        alphamerge.link_to(self.result)

        graph.configure()

        self.graph = graph

    def push_image(self, frame: av.VideoFrame):
        self.image.push(frame)

    def push_alpha(self, frame: av.VideoFrame):
        self.alpha.push(frame)

    def pull(self):
        try:
            return self.graph.pull()
        except BlockingIOError:
            return None


class NotAlphaMerger:
    def __init__(self, template: av.VideoStream):
        graph = av.filter.Graph()
        buffer = graph.add_buffer(template=template)

        null = graph.add("null")
        buffer.link_to(null)

        buffersink = graph.add("buffersink")
        null.link_to(buffersink)

        graph.configure()

        self.graph = graph

    def push_image(self, frame: av.VideoFrame):
        self.graph.push(frame)

    def push_alpha(self, frame: av.VideoFrame):
        raise NotImplementedError

    def pull(self):
        try:
            return self.graph.pull()
        except BlockingIOError:
            return None


def get_dst_size(dst_size: tuple[int, int], background_image: np.ndarray):
    target_height, target_width = background_image.shape[:2]

    width, height = dst_size
    if target_height / height < target_width / width:
        width = round(target_height / height * width)
        height = target_height
    else:
        height = round(target_width / width * height)
        width = target_width

    width, height = width - width % 16, height - height % 16

    bg_top = (target_height - height) // 2
    bg_left = (target_width - width) // 2

    return (width, height), background_image[
        bg_top : bg_top + height, bg_left : bg_left + width, :
    ]


def get_src_size(
    left: float,
    top: float,
    height: float,
    dst_size: tuple[int, int],
    src_size: tuple[int, int],
):
    dst_width, dst_height = dst_size
    src_width, src_height = src_size

    target_frame_height = dst_height * height
    frame_width = min(
        round(src_width * target_frame_height / src_height),
        dst_width,
    )
    frame_height = round(src_height * frame_width / src_width)

    left = (left + 1) / 2
    left_limit = dst_width - frame_width

    x = round(left * left_limit)
    y = round(top * dst_height)

    return (x, y), (frame_width, frame_height)


class BaseOverlayer:
    def __init__(
        self,
        background_image: np.ndarray,
        x: int,
        y: int,
        w: int,
        h: int,
    ):
        self.background_image = av.VideoFrame.from_ndarray(
            background_image,
            format="rgb24" if background_image.shape[-1] == 3 else "rgba",
        )

        self.graph = av.filter.Graph()
        self.src = self.graph.add_buffer(
            width=w,
            height=h,
            format="yuva420p",
            time_base=fractions.Fraction(1, 1000),
        )
        self.dst = self.graph.add_buffer(
            width=self.background_image.width,
            height=self.background_image.height,
            format=self.background_image.format.name,
            time_base=fractions.Fraction(1, 1000),
        )

        filtered = self.pre_overlay_filter(self.src)

        overlay = self.graph.add("overlay", f"{x}:{y}")
        self.dst.link_to(overlay, input_idx=0)
        filtered.link_to(overlay, input_idx=1)

        sink = self.graph.add("buffersink")
        overlay.link_to(sink)

        self.graph.configure()

    def pre_overlay_filter(self, context):
        return context

    def paste(self, src_image):
        src_image.pts = None
        self.src.push(src_image)
        self.dst.push(self.background_image)

        return self.graph.pull()

    def paste_video(self, iterator: list[av.VideoFrame]):
        for it in iterator:
            yield self.paste(it)

    @property
    def width(self):
        return self.background_image.width

    @property
    def height(self):
        return self.background_image.height


class Overlayer(BaseOverlayer):
    def __init__(
        self,
        background_image: np.ndarray,
        dst_size: tuple[int, int],
        src_size: tuple[int, int],
        left=0.0,
        top=0.0,
        height=1.0,
    ):
        origin_src_size = src_size
        dst_size, background_image = get_dst_size(dst_size, background_image)
        src_pos, src_size = get_src_size(left, top, height, dst_size, src_size)

        self.src_size = src_size

        super().__init__(
            background_image,
            x=src_pos[0],
            y=src_pos[1],
            w=origin_src_size[0],
            h=origin_src_size[1],
        )

    def pre_overlay_filter(self, context):
        scale = self.graph.add("scale", f"{self.src_size[0]}:{self.src_size[1]}")
        context.link_to(scale)
        return scale
