import { useState } from "react";
import { useNavigate } from "react-router-dom";

export default function UploadPage() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const uploadPDF = async () => {
    if (!file) {
      alert("Please select a PDF file");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/reorder-pdf", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    setLoading(false);

    if (data.error) {
      alert("Server Error: " + data.error);
      return;
    }

    
    navigate("/download", { state: { url: data.download_url } });
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Upload PDF to Reorder</h2>
      <input
        type="file"
        accept="application/pdf"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <br /><br />

      <button onClick={uploadPDF} disabled={loading}>
        {loading ? "Processing..." : "Upload & Reorder"}
      </button>
    </div>
  );
}
