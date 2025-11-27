import { useLocation } from "react-router-dom";

export default function DownloadPage() {
  const location = useLocation();
  const downloadUrl = location.state?.url;

  if (!downloadUrl) {
    return <h3>No processed PDF found. Upload again.</h3>;
  }

  const handleDownload = () => {
    window.location.href = "http://localhost:8000" + downloadUrl;
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>Your PDF is Ready</h2>
      <button onClick={handleDownload}>Download Reordered PDF</button>
    </div>
  );
}
