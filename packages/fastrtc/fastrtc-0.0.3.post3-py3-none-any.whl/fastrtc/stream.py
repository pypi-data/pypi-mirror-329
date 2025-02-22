import logging
from pathlib import Path
from typing import (
    Any,
    AsyncContextManager,
    Callable,
    Literal,
    cast,
    TypedDict,
)
from typing_extensions import NotRequired

import gradio as gr
from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from gradio import Blocks
from gradio.components.base import Component
from pydantic import BaseModel

from .tracks import StreamHandlerImpl, VideoEventHandler
from .webrtc import WebRTC
from .webrtc_connection_mixin import WebRTCConnectionMixin
from .websocket import WebSocketHandler

logger = logging.getLogger(__name__)

curr_dir = Path(__file__).parent


class Body(BaseModel):
    sdp: str
    type: str
    webrtc_id: str


class UIArgs(TypedDict):
    title: NotRequired[str]


class Stream(WebRTCConnectionMixin):
    def __init__(
        self,
        handler: VideoEventHandler | StreamHandlerImpl,
        *,
        additional_outputs_handler: Callable | None = None,
        mode: Literal["send-receive", "receive", "send"] = "send-receive",
        modality: Literal["video", "audio", "audio-video"] = "video",
        concurrency_limit: int | None | Literal["default"] = "default",
        time_limit: float | None = None,
        rtp_params: dict[str, Any] | None = None,
        rtc_configuration: dict[str, Any] | None = None,
        additional_inputs: list[Component] | None = None,
        additional_outputs: list[Component] | None = None,
        ui_args: UIArgs | None = None,
    ):
        self.mode = mode
        self.modality = modality
        self.rtp_params = rtp_params
        self.event_handler = handler
        self.concurrency_limit = cast(
            (int | float),
            1 if concurrency_limit in ["default", None] else concurrency_limit,
        )
        self.time_limit = time_limit
        self.additional_output_components = additional_outputs
        self.additional_input_components = additional_inputs
        self.additional_outputs_handler = additional_outputs_handler
        self.rtc_configuration = rtc_configuration
        self._ui = self._generate_default_ui(ui_args)

    def mount(self, app: FastAPI):
        app.router.post("/webrtc/offer")(self.offer)
        app.router.websocket("/telephone/handler")(self.telephone_handler)
        app.router.post("/telephone/incoming")(self.handle_incoming_call)
        app.router.websocket("/websocket/offer")(self.websocket_offer)
        lifespan = self._inject_startup_message(app.router.lifespan_context)
        app.router.lifespan_context = lifespan

    def _inject_startup_message(
        self, lifespan: Callable[[FastAPI], AsyncContextManager] | None = None
    ):
        import contextlib

        import click

        def print_startup_message():
            print(
                click.style("INFO", fg="green")
                + ":\t  Visit "
                + click.style(
                    "https://fastrtc.org/pr-preview/pr-60/userguide/api/", fg="cyan"
                )
                + " for WebRTC or Websocket API docs."
            )

        @contextlib.asynccontextmanager
        async def new_lifespan(app: FastAPI):
            if lifespan is None:
                print_startup_message()
                yield
            else:
                async with lifespan(app):
                    print_startup_message()
                    yield

        return new_lifespan

    def _generate_default_ui(
        self,
        ui_args: UIArgs | None = None,
    ):
        ui_args = ui_args or {}
        same_components = []
        additional_input_components = self.additional_input_components or []
        additional_output_components = self.additional_output_components or []
        if additional_output_components and not self.additional_outputs_handler:
            raise ValueError(
                "additional_outputs_handler must be provided if there are additional output components."
            )
        if additional_input_components and additional_output_components:
            same_components = [
                component
                for component in additional_input_components
                if component in additional_output_components
            ]
            for component in additional_output_components:
                if component not in same_components:
                    same_components.append(component)
        if self.modality == "video" and self.mode == "receive":
            with gr.Blocks() as demo:
                gr.HTML(
                    f"""
                <h1 style='text-align: center'>
                {ui_args.get("title", "Video Streaming (Powered by WebRTC ⚡️)")}
                </h1>
                """
                )
                with gr.Row():
                    if additional_input_components:
                        with gr.Column():
                            for component in additional_input_components:
                                component.render()
                            button = gr.Button("Start Stream", variant="primary")
                    with gr.Column():
                        output_video = WebRTC(
                            label="Video Stream",
                            rtc_configuration=self.rtc_configuration,
                            mode="receive",
                            modality="video",
                        )
                        for component in additional_output_components:
                            if component not in same_components:
                                component.render()
                output_video.stream(
                    fn=self.event_handler,
                    inputs=self.additional_input_components,
                    outputs=[output_video],
                    trigger=button.click,
                    time_limit=self.time_limit,
                    concurrency_limit=self.concurrency_limit,  # type: ignore
                )
                if additional_output_components:
                    assert self.additional_outputs_handler
                    output_video.on_additional_outputs(
                        self.additional_outputs_handler,
                        outputs=additional_output_components,
                    )
        elif self.modality == "video" and self.mode == "send":
            with gr.Blocks() as demo:
                gr.HTML(
                    f"""
                <h1 style='text-align: center'>
                {ui_args.get("title", "Video Streaming (Powered by WebRTC ⚡️)")}
                </h1>
                """
                )
                with gr.Row():
                    if additional_input_components:
                        with gr.Column():
                            for component in additional_input_components:
                                component.render()
                    with gr.Column():
                        output_video = WebRTC(
                            label="Video Stream",
                            rtc_configuration=self.rtc_configuration,
                            mode="send",
                            modality="video",
                        )
                        for component in additional_output_components:
                            if component not in same_components:
                                component.render()
                output_video.stream(
                    fn=self.event_handler,
                    inputs=[output_video] + additional_input_components,
                    outputs=[output_video],
                    time_limit=self.time_limit,
                    concurrency_limit=self.concurrency_limit,  # type: ignore
                )
                if additional_output_components:
                    assert self.additional_outputs_handler
                    output_video.on_additional_outputs(
                        self.additional_outputs_handler,
                        outputs=additional_output_components,
                    )
        elif self.modality == "video" and self.mode == "send-receive":
            css = """.my-group {max-width: 600px !important; max-height: 600 !important;}
                      .my-column {display: flex !important; justify-content: center !important; align-items: center !important};"""

            with gr.Blocks(css=css) as demo:
                gr.HTML(
                    f"""
                <h1 style='text-align: center'>
                {ui_args.get("title", "Video Streaming (Powered by WebRTC ⚡️)")}
                </h1>
                """
                )
                with gr.Column(elem_classes=["my-column"]):
                    with gr.Group(elem_classes=["my-group"]):
                        image = WebRTC(
                            label="Stream",
                            rtc_configuration=self.rtc_configuration,
                            mode="send-receive",
                            modality="video",
                        )
                        for component in additional_input_components:
                            component.render()
                if additional_output_components:
                    with gr.Column():
                        for component in additional_output_components:
                            if component not in same_components:
                                component.render()

                image.stream(
                    fn=self.event_handler,
                    inputs=[image] + additional_input_components,
                    outputs=[image],
                    time_limit=self.time_limit,
                    concurrency_limit=self.concurrency_limit,  # type: ignore
                )
                if additional_output_components:
                    assert self.additional_outputs_handler
                    image.on_additional_outputs(
                        self.additional_outputs_handler,
                        inputs=additional_output_components,
                        outputs=additional_output_components,
                    )
        elif self.modality == "audio" and self.mode == "receive":
            with gr.Blocks() as demo:
                gr.HTML(
                    """
                <h1 style='text-align: center'>
                FastAPI (Powered by WebRTC ⚡️)
                </h1>
                """
                )
                with gr.Row():
                    with gr.Column():
                        for component in additional_input_components:
                            component.render()
                        button = gr.Button("Start Stream", variant="primary")
                    if additional_output_components:
                        with gr.Column():
                            output_video = WebRTC(
                                label="Audio Stream",
                                rtc_configuration=self.rtc_configuration,
                                mode="receive",
                                modality="audio",
                            )
                            for component in additional_output_components:
                                if component not in same_components:
                                    component.render()
                output_video.stream(
                    fn=self.event_handler,
                    inputs=self.additional_input_components,
                    outputs=[output_video],
                    trigger=button.click,
                    time_limit=self.time_limit,
                    concurrency_limit=self.concurrency_limit,  # type: ignore
                )
                if additional_output_components:
                    assert self.additional_outputs_handler
                    output_video.on_additional_outputs(
                        self.additional_outputs_handler,
                        inputs=additional_output_components,
                        outputs=additional_output_components,
                    )
        elif self.modality == "audio" and self.mode == "send":
            with gr.Blocks() as demo:
                gr.HTML(
                    f"""
                <h1 style='text-align: center'>
                {ui_args.get("title", "Audio Streaming (Powered by WebRTC ⚡️)")}
                </h1>
                """
                )
                with gr.Row():
                    with gr.Column():
                        with gr.Group():
                            image = WebRTC(
                                label="Stream",
                                rtc_configuration=self.rtc_configuration,
                                mode="send-receive",
                                modality="audio",
                            )
                            for component in additional_input_components:
                                if component not in same_components:
                                    component.render()
                    if additional_output_components:
                        with gr.Column():
                            for component in additional_output_components:
                                component.render()
                image.stream(
                    fn=self.event_handler,
                    inputs=[image] + additional_input_components,
                    outputs=[image],
                    time_limit=self.time_limit,
                    concurrency_limit=self.concurrency_limit,  # type: ignore
                )
                if additional_output_components:
                    assert self.additional_outputs_handler
                    image.on_additional_outputs(
                        self.additional_outputs_handler,
                        inputs=additional_output_components,
                        outputs=additional_output_components,
                    )
        elif self.modality == "audio" and self.mode == "send-receive":
            with gr.Blocks() as demo:
                gr.HTML(
                    f"""
                <h1 style='text-align: center'>
                {ui_args.get("title", "Audio Streaming (Powered by WebRTC ⚡️)")}
                </h1>
                """
                )
                with gr.Row():
                    with gr.Column():
                        with gr.Group():
                            image = WebRTC(
                                label="Stream",
                                rtc_configuration=self.rtc_configuration,
                                mode="send-receive",
                                modality="audio",
                            )
                            for component in additional_input_components:
                                if component not in same_components:
                                    component.render()
                    if additional_output_components:
                        with gr.Column():
                            for component in additional_output_components:
                                component.render()

                    image.stream(
                        fn=self.event_handler,
                        inputs=[image] + additional_input_components,
                        outputs=[image],
                        time_limit=self.time_limit,
                        concurrency_limit=self.concurrency_limit,  # type: ignore
                    )
                    if additional_output_components:
                        assert self.additional_outputs_handler
                        image.on_additional_outputs(
                            self.additional_outputs_handler,
                            inputs=additional_output_components,
                            outputs=additional_output_components,
                        )
        return demo

    @property
    def ui(self) -> Blocks:
        return self._ui

    @ui.setter
    def ui(self, blocks: Blocks):
        self._ui = blocks

    async def offer(self, body: Body):
        return await self.handle_offer(
            body.model_dump(), set_outputs=self.set_additional_outputs(body.webrtc_id)
        )

    async def handle_incoming_call(self, request: Request):
        from twilio.twiml.voice_response import Connect, VoiceResponse

        response = VoiceResponse()
        response.say("Connecting to the AI assistant.")
        connect = Connect()
        connect.stream(url=f"wss://{request.url.hostname}/telephone/handler")
        response.append(connect)
        response.say("The call has been disconnected.")
        return HTMLResponse(content=str(response), media_type="application/xml")

    async def telephone_handler(self, websocket: WebSocket):
        handler = cast(StreamHandlerImpl, self.event_handler.copy())
        handler.phone_mode = True

        async def set_handler(s: str, a: WebSocketHandler):
            if len(self.connections) >= self.concurrency_limit:
                await cast(WebSocket, a.websocket).send_json(
                    {
                        "status": "failed",
                        "meta": {
                            "error": "concurrency_limit_reached",
                            "limit": self.concurrency_limit,
                        },
                    }
                )
                await websocket.close()
                return

        ws = WebSocketHandler(
            handler, set_handler, lambda s: None, lambda s: lambda a: None
        )
        await ws.handle_websocket(websocket)

    async def websocket_offer(self, websocket: WebSocket):
        handler = cast(StreamHandlerImpl, self.event_handler.copy())
        handler.phone_mode = False

        async def set_handler(s: str, a: WebSocketHandler):
            if len(self.connections) >= self.concurrency_limit:
                await cast(WebSocket, a.websocket).send_json(
                    {
                        "status": "failed",
                        "meta": {
                            "error": "concurrency_limit_reached",
                            "limit": self.concurrency_limit,
                        },
                    }
                )
                await websocket.close()
                return

            self.connections[s] = [a]  # type: ignore

        def clean_up(s):
            self.clean_up(s)

        ws = WebSocketHandler(
            handler, set_handler, clean_up, lambda s: self.set_additional_outputs(s)
        )
        await ws.handle_websocket(websocket)

    def fastphone(
        self,
        token: str | None = None,
        host: str = "127.0.0.1",
        port: int = 8000,
        **kwargs,
    ):
        import secrets
        import threading
        import time
        import urllib.parse

        import click
        import httpx
        import uvicorn
        from gradio.networking import setup_tunnel
        from gradio.tunneling import CURRENT_TUNNELS
        from huggingface_hub import get_token

        app = FastAPI()

        self.mount(app)

        t = threading.Thread(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": host, "port": port, **kwargs},
        )
        t.start()

        url = setup_tunnel(
            host, port, share_token=secrets.token_urlsafe(32), share_server_address=None
        )
        host = urllib.parse.urlparse(url).netloc

        # URL = "https://api.fastrtc.org"
        URL = "http://localhost:8082"
        r = httpx.post(
            URL + "/register",
            json={"url": host},
            headers={"Authorization": token or get_token() or ""},
        )
        r.raise_for_status()
        data = r.json()
        code = f"{data['code']}"
        phone_number = data["phone"]
        reset_date = data["reset_date"]
        print(
            click.style("INFO", fg="green")
            + ":\t  Your FastPhone is now live! Call "
            + click.style(phone_number, fg="cyan")
            + " and use code "
            + click.style(code, fg="cyan")
            + " to connect to your stream."
        )
        minutes = str(int(data["time_remaining"] // 60)).zfill(2)
        seconds = str(int(data["time_remaining"] % 60)).zfill(2)
        print(
            click.style("INFO", fg="green")
            + ":\t  You have "
            + click.style(f"{minutes}:{seconds}", fg="cyan")
            + " minutes remaining in your quota (Resetting on "
            + click.style(f"{reset_date}", fg="cyan")
            + ")"
        )
        print(
            click.style("INFO", fg="green")
            + ":\t  Visit "
            + click.style(
                "https://fastrtc.org/pr-preview/pr-60/userguide/audio/#telephone-integration",
                fg="cyan",
            )
            + " for information on making your handler compatible with phone usage."
        )
        try:
            while True:
                time.sleep(0.1)
        except (KeyboardInterrupt, OSError):
            print(
                click.style("INFO", fg="green")
                + ":\t  Keyboard interruption in main thread... closing server."
            )
            r = httpx.post(
                URL + "/unregister",
                json={"url": host, "code": code},
                headers={"Authorization": token or get_token() or ""},
            )
            t.join(timeout=5)
            for tunnel in CURRENT_TUNNELS:
                tunnel.kill()
