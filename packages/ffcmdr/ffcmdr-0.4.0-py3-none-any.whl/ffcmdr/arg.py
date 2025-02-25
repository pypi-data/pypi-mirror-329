from .cmd import FFmpegArg
from .cmd import FFmpegInput
from .cmd import ArgFlag

from .cmd import IArg
from .cmd import OArg
from .cmd import IOArg
from .cmd import GArg

"""
    TODO: Add from time to time cmd argument, maybe try to improve organisation
"""
# Print help / information / capabilities:
L, license = GArg("L"), GArg("license")
h, help = GArg("h"), GArg("help")
version = GArg("version")
muxers = GArg("muxers")
demuxers = GArg("demuxers")
devices = GArg("devices")
encoders = GArg("encoders")
decoders = GArg("decoders")
filters = GArg("filters")
pix_fmts = GArg("pix_fmts")
layouts = GArg("layouts")
sample_fmts = GArg("sample_fmts")

# Advanced information / capabilities:
buildconf = GArg("buildconf")
formats = GArg("formats")
codecs = GArg("codecs")
bsfs = GArg("bsfs")
protocols = GArg("protocols")
dispositions = GArg("dispositions")
colors = GArg("colors")
sources = GArg("sources")
sinks = GArg("sinks")
hwaccels = GArg("hwaccels")

# Global options (affect whole program instead of just one file):
v, loglevel = GArg("v"), GArg("loglevel")
y = GArg("y")
n = GArg("n")
stats = GArg("stats")

# Advanced global options:
report= GArg("report")
max_alloc = GArg("max_alloc")
cpuflags = GArg("cpuflag")
cpucount = GArg("cpucount")
hide_banner = GArg("hide_banner")
ignore_unknown = GArg("ignore_unknown")
copy_unknown = GArg("copy_unknown")
recast_media = GArg("recast_media")
benchmark = GArg("benchmark")
benchmark_all = GArg("benchmark_all")
progress = GArg("progress")
stdin = GArg("stdin")
timelimit = GArg("timelimit")
dump = GArg("dump")
hex = GArg("hex")
frame_drop_threshold = GArg("frame_drop_threshold")
copyts = GArg("copyts")
start_at_zero = GArg("start_at_zero")
copytb = GArg("copytb")
dts_delta_threshold = GArg("dts_delta_threshold")
dts_error_threshold = GArg("dts_error_threshold")
xerror = GArg("xerror")
abort_on = GArg("abort_on")
filter_threads = GArg("filter_threads")
filter_complex, lavfi = GArg("filter_complex"), GArg("lavfi")
filter_complex_threads = GArg("filter_complex_threads")
auto_conversion_filters = GArg("auto_conversion_filters")
stats_period = GArg("stats_period")
debug_ts = GArg("debug_ts")
max_error_rate = GArg("max_error_rate")
vstats = GArg("vstats")
vstats_file = GArg("vstats_file")
vstats_version = GArg("vstats_version")
sdp_file = GArg("sdp_file")
init_hw_device = GArg("init_hw_device")
filter_hw_device = GArg("filter_hw_device")

# Per-file options (input and output):
f = IOArg("f")
t = IOArg("t")
to = IOArg("to")
ss = IOArg("ss")

# Advanced per-file options (input and output):
i = FFmpegInput()
bitexact = IOArg("bitexact")
thread_queue_size = IOArg("thread_queue_size")

# Advanced per-file options (input-only):
sseof = IArg("sseof")
seek_timestamp = IArg("seek_timestamp")
accurate_seek = IArg("accurate_seek")
isync = IArg("isync")
itsoffset = IArg("itsoffset")
re = IArg("re")
readrate = IArg("readrate")
readrate_initial_burst = IArg("readrate_initial_burst")
dump_attachment = IArg("dump_attachment")
stream_loop = IArg("stream_loop")
find_stream_info = IArg("find_stream_info")

# Per-file options (output-only):
metadata = OArg("metadata")

# Advanced per-file options (output-only):
map = OArg("map")
map_metadata = OArg("map_metadata")
map_chapters = OArg("map_chapters")
fs = OArg("fs")
timestamp = OArg("timestamp")
program = OArg("program")
stream_group = OArg("stream_group")
dframes = OArg("frames")["d"]
target = OArg("target")
shortest = OArg("shortest")
shortest_buf_duration = OArg("shortest_buf_duration")
qscale = OArg("qscale")
profile= OArg("profile")
attach = OArg("attach")
muxdelay = OArg("muxdelay")
muxpreload = OArg("muxpreload")
fpre = OArg("fpre")

# Per-stream options:
c, codec = IOArg("c"), IOArg("codec")
filter = OArg("filter")

# Advanced per-stream options:
pre = OArg("pre")
itsscale = IArg("itsscale")
copyinkf = OArg("copyinkf")
copypriorss = IOArg("copypriorss") # Undocumented
frames = OArg("frames")
tag = IOArg("tag")
q = OArg("q")
reinit_filter = IArg("reinit_filter")
discard = IArg("discard")
disposition = OArg("disposition")
bits_per_raw_sample = OArg("bits_per_raw_sample")
stats_enc_pre = OArg("stats_enc_pre")
stats_enc_post = OArg("stats_enc_post")
stats_mux_pre = OArg("stats_mux_pre")
stats_enc_pre_fmt = OArg("stats_enc_pre_fmt")
stats_enc_post_fmt = OArg("stats_enc_post_fmt")
stats_mux_pre_fmt = OArg("stats_mux_pre_fmt")
time_base = IOArg("time_base") # Undocumented
enc_time_base = OArg("enc_time_base")
bsf = IOArg("bsf")
max_muxing_queue_size = OArg("max_muxing_queue_size")
muxing_queue_data_threshold = OArg("muxing_queue_data_threshold")

# Video options:

r = IOArg("r")
aspect = OArg("aspect")
vn = IOArg("vn")
vcodec = OArg("vcodec")
vf = OArg("vf")
b = IOArg("b")

# Advanced Video options:
vframes = frames['v']
fpsmax = OArg("fpsmax")
pix_fmt = IOArg("pix_fmt")
display_rotation = IArg("display_rotation")
display_hflip = IArg("display_hflip")
display_vflip = IArg("display_vflip")
rc_override = OArg("rc_override")
timecode = GArg("timecode")
pass_ = OArg("pass")
passlogfile = OArg("passlogfile")
intra_matrix = IOArg("intra_matrix")
inter_matrix = IOArg("inter_matrix")
chroma_intra_matrix = IOArg("chroma_intra_matrix")
vtag = OArg("vtag")
fps_mode = OArg("fps_mode")
force_fps = IOArg("force_fps") # Undocumented
streamid = OArg("streamid")
force_key_frames = OArg("force_key_frames")
hwaccel = IArg("hwaccel")
hwaccel_device = IArg("hwaccel_device")
hwaccel_output_format = IOArg("hwaccel_output_format")
autorotate = IOArg("autorotate")
autoscale = IOArg("autoscale")
apply_cropping = IArg("apply_cropping")
fix_sub_duration_heartbeat = IOArg("fix_sub_duration_heartbeat")
vpre = IOArg("vpre")

# Audio options:
aq = OArg("aq")
ar = IOArg("ar")
ac = IOArg("ac")
an = IOArg("an")
ab = IOArg("ab")
af = OArg("af")
acodec = IOArg("acodec")

# Advanced Audio options:
aframes = OArg("aframes")
apad = OArg("apad")
atag = OArg("atag")
sample_fmt = OArg("sample_fmt")
channel_layout = IOArg("channel_layout")
ch_layout = IOArg("ch_layout")
guess_layout_max = IArg("guess_layout_max")
apre = IOArg("apre")

# Subtitle options:
sn = IOArg("sn")
scodec = IOArg("scodec")

# Advanced Subtitle options:
stag = IOArg("stag") # Undocumented
fix_sub_duration = IOArg("fix_sub_duration")
canvas_size = IOArg("canvas_size")
spre = IOArg("spre")

# Data stream options:
dcodec = c['d']
dn = IOArg("dn")

# AVCodecContext AVOptions:
flags = OArg("flags")
flags2 = OArg("flags2")
export_side_data = OArg("export_side_data")
g = OArg("g")
cutoff = OArg("cutoff")
frame_size = OArg("frame_size")
qcomp = OArg("qcomp")
qblur = OArg("qblur")
qmin = OArg("qmin")
qmax = OArg("qmax")
qdiff = OArg("qdiff")
bf = OArg("bf")
b_qfactor = OArg("b_qfactor")
bug = OArg("bug")
strict = OArg("strict")
b_qoffset = OArg("b_qoffset")
err_detect = OArg("err_detect")
maxrate = OArg("maxrate")
minrate = OArg("minrate")
bufsize = OArg("bufsize")
i_qfactor = OArg("i_qfactor")
i_qoffset = OArg("i_qoffset")
dct = OArg("dct")
lumi_mask = OArg("lumi_mask")
tcplx_mask = OArg("tcplx_mask")
scplx_mask = OArg("scplx_mask")
p_mask = OArg("p_mask")
dark_mask = OArg("dark_mask")
idct= OArg("idct")
ec = OArg("ec")
sar = OArg("sar")
debug = OArg("debug")
################################################################
# AVOptions https://ffmpeg.org/ffmpeg.html#AVOptions

s = IOArg("s")


# Advanced Video options https://ffmpeg.org/ffmpeg.html#Advanced-Video-options

sws_flags = IOArg("sws_flags")

# Advanced options https://ffmpeg.org/ffmpeg.html#Advanced-options

vsync = GArg("vsync")
update = OArg("update")

## FFProbe
show_error = GArg("show_error")
show_format = GArg("show_format")
show_streams = GArg("show_streams")
print_format = GArg("print_format")

## Other
movflags = OArg("movflags")
loop = IOArg("loop")