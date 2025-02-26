mod client;
mod http;
mod request;
mod ws;

pub use self::request::{execute_request2, execute_websocket_request2};
pub use self::{
    client::Client,
    http::{Response, Streamer},
    ws::{Message, WebSocket},
};
use crate::param::{RequestParams, WebSocketParams};
use crate::types::{LookupIpStrategy, Method};
use crate::{apply_option, dns};
use request::{execute_request, execute_websocket_request};
use std::sync::LazyLock;

static DEFAULT_CLIENT: LazyLock<rquest::Client> = LazyLock::new(|| {
    let mut builder = rquest::Client::builder();
    apply_option!(
        apply_if_ok,
        builder,
        || dns::get_or_try_init(LookupIpStrategy::Ipv4AndIpv6),
        dns_resolver
    );
    builder
        .no_hickory_dns()
        .no_keepalive()
        .build()
        .expect("Failed to build the default client.")
});

/// Send a shortcut HTTP request.
#[inline(always)]
pub async fn shortcut_request<U>(
    url: U,
    method: Method,
    params: Option<RequestParams>,
) -> crate::Result<Response>
where
    U: AsRef<str>,
{
    execute_request(&*DEFAULT_CLIENT, method, url.as_ref().to_string(), params).await
}

/// Send a shortcut WebSocket request.
#[inline(always)]
pub async fn shortcut_websocket_request<U>(
    url: U,
    params: Option<WebSocketParams>,
) -> crate::Result<WebSocket>
where
    U: AsRef<str>,
{
    execute_websocket_request(&*DEFAULT_CLIENT, url.as_ref().to_string(), params).await
}
