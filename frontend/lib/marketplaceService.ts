const API_BASE = '/api';

export async function getPendingLawyers() {
    const response = await fetch(`${API_BASE}/admin/marketplace/pending`);
    if (!response.ok) throw new Error('Failed to fetch pending lawyers');
    return response.json();
}

export async function verifyLawyer(lawyerId: string | number) {
    const response = await fetch(`${API_BASE}/admin/marketplace/verify/${lawyerId}`, {
        method: 'POST',
    });
    if (!response.ok) throw new Error('Failed to verify lawyer');
    return response.json();
}

export async function rejectLawyer(lawyerId: string | number, reason: string) {
    const response = await fetch(`${API_BASE}/admin/marketplace/reject/${lawyerId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reason }),
    });
    if (!response.ok) throw new Error('Failed to reject lawyer');
    return response.json();
}
