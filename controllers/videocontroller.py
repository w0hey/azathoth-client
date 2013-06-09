import logging

import gtk
import pygst
pygst.require("0.10")
import gst

from gtkmvc import Controller

class VideoController(Controller):

    tempcaps = gst.Caps("application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)MP4V-ES, profile-level-id=(string)5, payload=(int)96")

    def register_view(self, view):
        self.videoWindow = self.view.get_top_widget()
        self.videoWindow.show_all()
        self.startVideo()

    def startVideo(self):
        self.player = gst.Pipeline("player")
        source = gst.element_factory_make("udpsrc", "udp-source")
        depayloader = gst.element_factory_make("rtpmp4vdepay", "mp4vdepay")
        decoder = gst.element_factory_make("ffdec_mpeg4", "mpeg4-decoder")
        colorspace = gst.element_factory_make("ffmpegcolorspace", "colorspace")
        sink = gst.element_factory_make("ximagesink", "video-output")
        self.player.add(source, depayloader, decoder, colorspace, sink)
        gst.element_link_many(source, depayloader, decoder, colorspace, sink)
        
        bus = self.player.get_bus()
        bus.enable_sync_message_emission()
        bus.add_signal_watch()
        bus.connect("message", self.on_message)
        logging.debug("foo")
        bus.connect("sync-message::element", self.on_sync_message)

        source.set_property("port", 5099)
        source.set_property("caps", self.tempcaps)
        self.player.set_state(gst.STATE_PLAYING)
    
    def on_message(self, bus, message):
        t = message.type
        if t == gst.MESSAGE_EOS:
            self.player.set_state(gst.STATE_NULL)
        elif t == gst.MESSAGE_ERROR:
            self.player.set_state(gst.STATE_NULL)

    def on_sync_message(self, bus, message):
        if message.structure is None:
            return
        message_name = message.structure.get_name()
        if message_name == "prepare-xwindow-id":
            imagesink = message.src
            imagesink.set_property("force-aspect_ratio", True)
            gtk.gdk.threads_enter()
            gtk.gdk.display_get_default().sync()
            imagesink.set_xwindow_id(self.videoWindow.window.xid)
            logging.debug("xid: " + str(self.videoWindow.window.xid))
            gtk.gdk.threads_leave()
