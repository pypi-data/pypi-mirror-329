from rest_framework.request import Request


def get_client_ip(request: Request):
    ip = request.headers.get('CF-Connecting-IP')
    if ip:
        return ip

    x_forwarded_for = request.headers.get('X-Forwarded-For')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        return ip

    ip = request.headers.get('X-Real-IP')
    if ip:
        return ip
    return request.META.get('REMOTE_ADDR')
