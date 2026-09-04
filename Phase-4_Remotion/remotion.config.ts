import { Config } from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setChromiumOpenGlRenderer('angle');
Config.setPixelFormat('yuv420p');
Config.setCodec('h264');
Config.setAudioCodec('aac');
Config.setAudioBitrate('192k');
