from .session_handle import Custom_Session

def bag(request):
    return {"bag":Custom_Session(request)}