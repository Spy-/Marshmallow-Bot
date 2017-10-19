from discord import opus


def load_opus_lib():

    OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll',
                 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

    if opus.is_loaded():
        return True

    for opus_lib in OPUS_LIBS:
        try:
            opus.load_opus(opus_lib)
            return
        except OSError:
            pass

    raise RuntimeError('Could not load an opus lib. Tried %s' %
                       (', '.join(OPUS_LIBS)))
