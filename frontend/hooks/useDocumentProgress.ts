import { useEffect, useState } from 'react';

interface ProgressData {
    document_id: number;
    filename: string;
    progress: number;
    status: string;
    document_type?: string;
    confidence?: number;
    error_message?: string;
}

export function useDocumentProgress(documentId: number | null) {
    const [progress, setProgress] = useState<ProgressData>({
        document_id: 0,
        filename: '',
        progress: 0,
        status: 'pending'
    });
    const [isConnected, setIsConnected] = useState(false);
    const [usePolling, setUsePolling] = useState(false);

    useEffect(() => {
        if (!documentId) return;

        let ws: WebSocket | null = null;
        let pollInterval: NodeJS.Timeout | null = null;

        // Try WebSocket first
        const connectWebSocket = () => {
            try {
                const wsUrl = `ws://localhost:8002/ws/document/${documentId}`;
                ws = new WebSocket(wsUrl);

                ws.onopen = () => {
                    console.log('✅ WebSocket connected');
                    setIsConnected(true);
                    setUsePolling(false);
                };

                ws.onmessage = (event) => {
                    const data = JSON.parse(event.data);
                    setProgress(data);

                    // If completed or failed, close connection
                    if (data.status === 'completed' || data.status === 'failed') {
                        console.log(`✅ Document processing ${data.status}`);
                        ws?.close();
                    }
                };

                ws.onerror = (error) => {
                    console.warn('⚠️ WebSocket error, falling back to polling:', error);
                    setIsConnected(false);
                    setUsePolling(true);
                };

                ws.onclose = () => {
                    console.log('❌ WebSocket disconnected');
                    setIsConnected(false);
                };
            } catch (error) {
                console.warn('⚠️ WebSocket failed, using polling:', error);
                setUsePolling(true);
            }
        };

        // Fallback: Polling if WebSocket doesn't work
        const startPolling = () => {
            pollInterval = setInterval(async () => {
                try {
                    const token = localStorage.getItem('token');
                    const response = await fetch(`/api/documents/${documentId}/progress`, {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        const data = await response.json();
                        setProgress(data);

                        // Stop polling if complete
                        if (data.status === 'completed' || data.status === 'failed') {
                            if (pollInterval) clearInterval(pollInterval);
                        }
                    }
                } catch (error) {
                    console.error('Polling error:', error);
                }
            }, 2000); // Poll every 2 seconds
        };

        // Start connection
        if (!usePolling) {
            connectWebSocket();
        } else {
            startPolling();
        }

        // Cleanup
        return () => {
            if (ws) {
                ws.close();
            }
            if (pollInterval) {
                clearInterval(pollInterval);
            }
        };
    }, [documentId, usePolling]);

    return { progress, isConnected, usePolling };
}
