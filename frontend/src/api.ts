import axios from 'axios';

const API_URL = 'http://localhost:8000/api';

export const api = axios.create({
  baseURL: API_URL,
});

export interface Transaction {
  id?: number;
  date: string;
  description: string;
  category: string;
  spender: string;
  payer: string;
  amount: number;
  owed_amount: number;
  comment?: string;
  source: string;
}

export interface Stats {
  spending_by_category: { category: string; total: number }[];
  debt_summary: { debtor: string; creditor: string; amount: number }[];
}

export const uploadHistory = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  return api.post('/upload/history', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
};

export const uploadStatement = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);
  const response = await api.post<Transaction[]>('/upload/statement', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });
  return response.data;
};

export const saveTransactions = async (transactions: Transaction[]) => {
  return api.post('/transactions/bulk', transactions);
};

export const getTransactions = async () => {
  const response = await api.get<Transaction[]>('/transactions');
  return response.data;
};

export const getStats = async () => {
  const response = await api.get<Stats>('/stats');
  return response.data;
};
