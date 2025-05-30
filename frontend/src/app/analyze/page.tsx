'use client';

import { useState, useEffect } from "react";

type Opinion = {
  type: string;
  text: string;
};

type TopicResult = {
  topic_id: string;
  topic_summary: string;
  opinions: Opinion[];
  conclusion: string;
};

type AnalyzeResponse = {
  topics: TopicResult[];
};

export default function AnalyzePage() {
  const [comments, setComments] = useState("");
  const [requestId, setRequestId] = useState<string | null>(null);
  const [finalResult, setFinalResult] = useState<AnalyzeResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [waiting, setWaiting] = useState(false);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8080";

  const handleAnalyze = async () => {
    setLoading(true);
    setFinalResult(null);
    setRequestId(null);
    setWaiting(false);

    const response = await fetch(`${API_URL}/analyze`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        comments: comments.split('\n').filter(Boolean)
      }),
    });

    const data = await response.json();
    setRequestId(data.request_id);
    setLoading(false);
    setWaiting(true);
  };

  useEffect(() => {
    if (!requestId) return;
    setWaiting(true);
    const interval = setInterval(async () => {
      const res = await fetch(`${API_URL}/results/${requestId}`);
      const data = await res.json();
      if (data.result) {
        setFinalResult(data.result);
        setWaiting(false);
        clearInterval(interval);
      }
    }, 3000); 
    return () => clearInterval(interval);
  }, [requestId]);

  return (
    <div className="min-h-screen flex bg-[#18181b] text-white">
      <div className="w-1/2 p-8 flex flex-col">
        <h2 className="text-xl font-semibold mb-4">Paste Comments</h2>
        <textarea
          className="w-full h-[320px] bg-[#23272f] text-white rounded-xl p-4 mb-4"
          placeholder="Each comment on a new line..."
          value={comments}
          onChange={e => setComments(e.target.value)}
        />
        <button
          onClick={handleAnalyze}
          className="px-8 py-3 mt-2 rounded-xl text-lg font-bold bg-gradient-to-r from-blue-500 via-cyan-400 to-blue-600 bg-[length:200%_200%] animate-gradient-move shadow-lg hover:scale-105 transition-transform disabled:opacity-60"
          disabled={loading || !comments.trim() || waiting}
        >
          {loading || waiting ? (
            <span className="flex items-center gap-2">
              <Spinner />
              {loading ? "Sending..." : "Analyzing..."}
            </span>
          ) : "Analyze"}
        </button>
        {waiting && !finalResult && (
          <span className="text-sm text-gray-400 mt-4">Your request is being processed. This may take a while...</span>
        )}
      </div>
      <div className="w-1/2 p-8 flex flex-col border-l border-gray-700">
        <h2 className="text-xl font-semibold mb-4">Results</h2>
        {waiting && !finalResult && <Spinner />}
        {finalResult && (
          <pre className="whitespace-pre-wrap bg-[#23272f] p-4 rounded-xl">{JSON.stringify(finalResult, null, 2)}</pre>
        )}
      </div>
      <style jsx global>{`
        @keyframes gradient-move {
          0% { background-position: 0% 50%; }
          50% { background-position: 100% 50%; }
          100% { background-position: 0% 50%; }
        }
        .animate-gradient-move {
          animation: gradient-move 3s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
}

function Spinner() {
  return (
    <svg className="animate-spin h-5 w-5 text-blue-400" fill="none" viewBox="0 0 24 24">
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"/>
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z"/>
    </svg>
  );
}
