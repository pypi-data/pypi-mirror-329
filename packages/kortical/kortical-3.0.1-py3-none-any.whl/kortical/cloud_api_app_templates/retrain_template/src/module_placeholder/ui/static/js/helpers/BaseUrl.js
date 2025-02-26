export function get_base_url() {
    const current_url = new URL(window.location.href);
    const path_segments = current_url.pathname.split('/');
    path_segments.pop();
    const base_url = current_url.origin + path_segments.join('/');
    return base_url;
}