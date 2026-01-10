import React, { useState } from 'react';
import { uploadHistory, uploadStatement, saveTransactions } from './api';
import type { Transaction } from './api';
import { useNavigate } from 'react-router-dom';

const Upload: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [type, setType] = useState<'history' | 'statement'>('history');
  const [parsedTxns, setParsedTxns] = useState<Transaction[]>([]);
  const [globalPayer, setGlobalPayer] = useState<string>('Vishal');
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) return;

    if (type === 'history') {
      try {
        await uploadHistory(file);
        alert('History uploaded successfully!');
        navigate('/');
      } catch (e) {
        alert('Error uploading history');
        console.error(e);
      }
    } else {
      try {
        const data = await uploadStatement(file);
        // Pre-fill data
        const enriched = data.map(t => ({
          ...t,
          payer: globalPayer,
          spender: 'Shared', // Default
          owed_amount: t.amount / 2,
        }));
        setParsedTxns(enriched);
      } catch (e) {
        alert('Error parsing statement');
        console.error(e);
      }
    }
  };

  const handleSave = async () => {
    try {
      await saveTransactions(parsedTxns);
      alert('Transactions saved!');
      navigate('/');
    } catch (e) {
      alert('Error saving transactions');
    }
  };

  const updateTxn = (index: number, field: keyof Transaction, value: any) => {
    const newTxns = [...parsedTxns];
    const txn = { ...newTxns[index], [field]: value };

    // Auto-calc owed amount if spender/payer changes
    if (field === 'spender' || field === 'payer' || field === 'amount') {
      if (txn.spender === 'Shared') {
        txn.owed_amount = txn.amount / 2;
      } else if (txn.spender === txn.payer) {
        txn.owed_amount = 0;
      } else {
        txn.owed_amount = txn.amount;
      }
    }

    newTxns[index] = txn;
    setParsedTxns(newTxns);
  };

  if (parsedTxns.length > 0) {
    return (
      <div className="p-4">
        <h2 className="text-xl font-bold mb-4">Review Transactions</h2>
        <div className="overflow-x-auto">
          <table className="min-w-full bg-white border">
            <thead>
              <tr>
                <th className="p-2 border">Date</th>
                <th className="p-2 border">Description</th>
                <th className="p-2 border">Amount</th>
                <th className="p-2 border">Category</th>
                <th className="p-2 border">Spender</th>
                <th className="p-2 border">Payer</th>
                <th className="p-2 border">Owed</th>
              </tr>
            </thead>
            <tbody>
              {parsedTxns.map((txn, idx) => (
                <tr key={idx}>
                  <td className="p-2 border">{txn.date}</td>
                  <td className="p-2 border">{txn.description}</td>
                  <td className="p-2 border">${txn.amount.toFixed(2)}</td>
                  <td className="p-2 border">
                    <input
                      className="border p-1 w-full"
                      value={txn.category}
                      onChange={(e) => updateTxn(idx, 'category', e.target.value)}
                    />
                  </td>
                  <td className="p-2 border">
                    <select
                      className="border p-1 w-full"
                      value={txn.spender}
                      onChange={(e) => updateTxn(idx, 'spender', e.target.value)}
                    >
                      <option value="Shared">Shared</option>
                      <option value="Vishal">Vishal</option>
                      <option value="Gouthami">Gouthami</option>
                    </select>
                  </td>
                  <td className="p-2 border">
                    <select
                      className="border p-1 w-full"
                      value={txn.payer}
                      onChange={(e) => updateTxn(idx, 'payer', e.target.value)}
                    >
                      <option value="Vishal">Vishal</option>
                      <option value="Gouthami">Gouthami</option>
                    </select>
                  </td>
                  <td className="p-2 border text-gray-500">${txn.owed_amount.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <button
          onClick={handleSave}
          className="mt-4 bg-green-500 text-white px-4 py-2 rounded"
        >
          Save All
        </button>
      </div>
    );
  }

  return (
    <div className="p-4 max-w-md mx-auto">
      <h2 className="text-xl font-bold mb-4">Upload Data</h2>

      <div className="mb-4">
        <label className="block mb-2">Upload Type</label>
        <select
          className="border p-2 w-full"
          value={type}
          onChange={(e) => setType(e.target.value as any)}
        >
          <option value="history">Historical Data (CSV)</option>
          <option value="statement">New Statement (PDF)</option>
        </select>
      </div>

      {type === 'statement' && (
        <div className="mb-4">
          <label className="block mb-2">Who Paid this Statement?</label>
          <select
            className="border p-2 w-full"
            value={globalPayer}
            onChange={(e) => setGlobalPayer(e.target.value)}
          >
            <option value="Vishal">Vishal</option>
            <option value="Gouthami">Gouthami</option>
          </select>
        </div>
      )}

      <div className="mb-4">
        <input
          type="file"
          onChange={(e) => setFile(e.target.files ? e.target.files[0] : null)}
          className="border p-2 w-full"
        />
      </div>

      <button
        onClick={handleUpload}
        disabled={!file}
        className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-300"
      >
        Upload & Process
      </button>
    </div>
  );
};

export default Upload;
