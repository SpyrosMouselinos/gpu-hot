"""WebSocket handlers for hub mode"""

import eventlet
import logging

logger = logging.getLogger(__name__)


def register_hub_handlers(socketio, hub):
    """Register SocketIO event handlers for hub mode"""
    
    @socketio.on('connect')
    def on_connect():
        logger.debug('Dashboard client connected')
        if not hub.running:
            hub.running = True
            socketio.start_background_task(hub_loop, socketio, hub)
    
    @socketio.on('disconnect')
    def on_disconnect():
        logger.debug('Dashboard client disconnected')


def hub_loop(socketio, hub):
    """Background loop that emits aggregated cluster data"""
    logger.info("Hub monitoring loop started")
    
    while hub.running:
        try:
            cluster_data = hub.get_cluster_data()
            socketio.emit('gpu_data', cluster_data, namespace='/')
        except Exception as e:
            logger.error(f"Error in hub loop: {e}")
        
        # Match node update rate for real-time responsiveness
        eventlet.sleep(0.5)

