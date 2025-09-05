// frontend/src/app/page.tsx
"use client";

import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { Upload } from "lucide-react";
import axios from "axios";

export default function Home() {
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [uploadStatus, setUploadStatus] = useState("");
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState<number | null>(null);

  const handleUpload = async () => {
    if (!pdfFile) return;
    setUploadStatus("Uploading...");
    setUploadProgress(0); // Start with 0%

    const formData = new FormData();
    formData.append("file", pdfFile);

    try {
      //const response = await axios.post("http://localhost:8000/upload", formData);
      await axios.post("http://localhost:8000/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setUploadProgress(percent);
          }
        },
      });

      setUploadStatus("✅ PDF uploaded and processed");

      setTimeout(() => {
        setUploadStatus("✅ PDF uploaded and processed");
        setUploadProgress(null); // Reset progress bar
      }, 1500); // Optional delay: adjust based on backend speed

    } catch (error) {
      setUploadStatus("❌ Upload failed");
      setUploadProgress(null);

    }
  };

  const handleQuery = async () => {
    if (!question) return;
    setLoading(true);
    setAnswer("");
    try {
      const response = await axios.get("http://localhost:8000/query", {
        params: { q: question },
      });
      setAnswer(response.data.answer);
    } catch (error) {
      setAnswer("Failed to get answer");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-2xl mx-auto space-y-8">
        <h1 className="text-3xl font-bold text-center">PDF QA Assistant</h1>

        {/* Upload Section */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <Label htmlFor="pdf">Upload a PDF</Label>
            <Input
              type="file"
              accept="application/pdf"
              onChange={(e) => setPdfFile(e.target.files?.[0] || null)}
            />
            <Button onClick={handleUpload} disabled={!pdfFile}>
              <Upload className="mr-2 h-4 w-4" /> Upload
            </Button>
            {uploadStatus && <p>{uploadStatus}</p>}
            {uploadProgress !== null && (
              <div className="w-full bg-gray-300 rounded h-3">
                <div
                  className="bg-blue-500 h-3 rounded"
                  style={{ width: `${uploadProgress}%` }}
                />
                <p className="text-sm text-gray-600 mt-1">{uploadProgress}%</p>
              </div>
            )}
          </CardContent>
        </Card>

        {/* QA Section */}
        <Card>
          <CardContent className="p-6 space-y-4">
            <Label htmlFor="question">Ask a Question</Label>
            <Textarea
              id="question"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="e.g., What is the main topic of the PDF?"
            />
            <Button onClick={handleQuery} disabled={loading || !question}>
              {loading ? "Thinking..." : "Ask"}
            </Button>
            {answer && (
              <div className="border p-4 rounded bg-white shadow">
                <p className="font-semibold">Answer:</p>
                <p>{answer}</p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}