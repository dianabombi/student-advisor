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

export async function searchLawyers(filters?: Record<string, string>) {
    const params = new URLSearchParams(filters || {});
    const response = await fetch(`${API_BASE}/marketplace/lawyers?${params}`);
    if (!response.ok) throw new Error('Failed to search lawyers');
    return response.json();
}

export async function getLawyerProfile(lawyerId: string | number) {
    const response = await fetch(`${API_BASE}/marketplace/lawyers/${lawyerId}`);
    if (!response.ok) throw new Error('Failed to get lawyer profile');
    return response.json();
}

export async function registerLawyer(data: Record<string, unknown>) {
    const response = await fetch(`${API_BASE}/marketplace/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to register lawyer');
    return response.json();
}

export async function getLawyerDashboard() {
    const response = await fetch(`${API_BASE}/marketplace/dashboard`);
    if (!response.ok) throw new Error('Failed to get lawyer dashboard');
    return response.json();
}

export async function updateLawyerAvailability(available: boolean) {
    const response = await fetch(`${API_BASE}/marketplace/availability`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ available }),
    });
    if (!response.ok) throw new Error('Failed to update availability');
    return response.json();
}
