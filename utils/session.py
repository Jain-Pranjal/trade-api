from datetime import datetime

sessions = {}

# This will track sessions
def track_session(ip: str):
    """Track user session by IP address"""
    now = datetime.utcnow()
    if ip in sessions:
        sessions[ip]['last_active'] = now
        sessions[ip]['request_count'] += 1
    else:
        sessions[ip] = {
            'first_active': now,
            'last_active': now,
            'request_count': 1
        }
    return sessions[ip]



def get_session_info(ip: str) -> dict:
    """Get session information for an IP address"""
    if ip in sessions:
        session = sessions[ip]
        return {
            'request_count': session['request_count'],
            'first_active': session['first_active'].isoformat(),
            'last_active': session['last_active'].isoformat()
        }
    return None