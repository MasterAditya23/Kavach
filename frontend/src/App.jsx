import "./App.css"
import { useState } from "react"

function App() {
  const [message, setMessage] = useState("")
  const [analysis, setAnalysis] = useState(null)
  const [qrFile, setQrFile] = useState(null)
  const [apkFile, setApkFile] = useState(null)
  return (
    <div className="app">
      <header className="header">
        <div>
          <h1>KAVACH</h1>
          <p>Multi-Vector Fraud Detection</p>
        </div>
      </header>

      <main className="main">
        <section className="hero">
          <h2>Detect digital threats before you act</h2>
          <p>
            Analyze suspicious QR codes, APK files, and messages using
            technical evidence, AI reasoning, and risk analysis.
          </p>
        </section>

        <section className="scanner-grid">
         <div className="scanner-card">
  <div className="icon">▣</div>
  <h3>QR Scanner</h3>
  <p>
    Scan a QR image and analyze the extracted URL or data for
    suspicious indicators.
  </p>

<div className="upload-zone qr-upload-zone">
  <div className="upload-icon">☁</div>

  <div className="upload-title">
    Choose a QR image
  </div>

  <div className="upload-subtitle">
    JPG, PNG images supported
  </div>

  <label className="browse-button">
    <span>▣</span>
    Browse Files
    <input
      type="file"
      accept="image/*"
      onChange={(e) => setQrFile(e.target.files[0])}
    />
  </label>

  {qrFile && (
    <div className="selected-file">
      ✓ {qrFile.name}
    </div>
  )}
</div>

  <button
  onClick={async () => {
    if (!qrFile) {
      alert("Please select a QR image first.")
      return
    }

    const formData = new FormData()
    formData.append("file", qrFile)

    const response = await fetch(
      "https://kavach-te0g.onrender.com/api/analyze/qr",
      {
        method: "POST",
        body: formData,
      }
    )

    const data = await response.json()

    setAnalysis({
  ...data.analysis,
  decoded_data: data.decoded_data,
})
  }}
>
  Scan QR Code
</button>
</div>

         <div className="scanner-card">
  <div className="icon">▤</div>
  <h3>APK Scanner</h3>
  <p>
    Analyze an APK's manifest and permissions to identify
    potentially suspicious behavior.
  </p>

<div className="upload-zone apk-upload-zone">
  <div className="upload-icon">☁</div>

  <div className="upload-title">
    Choose an APK file
  </div>

  <div className="upload-subtitle">
    .apk files supported
  </div>

  <label className="browse-button">
    <span>▣</span>
    Browse Files
    <input
      type="file"
      accept=".apk"
      onChange={(e) => setApkFile(e.target.files[0])}
    />
  </label>

  {apkFile && (
    <div className="selected-file">
      ✓ {apkFile.name}
    </div>
  )}
</div>

  <button
  onClick={async () => {
    if (!apkFile) {
      alert("Please select an APK file first.")
      return
    }

    const formData = new FormData()
    formData.append("file", apkFile)

    const response = await fetch(
      "https://kavach-te0g.onrender.com/api/analyze/apk",
      {
        method: "POST",
        body: formData,
      }
    )

    const data = await response.json()

    setAnalysis({
      ...data.analysis,
      package_name: data.package_name,
      permissions: data.permissions,
      apk_findings: data.findings,
    })
  }}
>
  Analyze APK
</button>
</div>

         <div className="scanner-card">
  <div className="icon">☷</div>
  <h3>Chat Scanner</h3>
  <p>
    Analyze suspicious messages or call transcripts for
    social-engineering and scam patterns.
  </p>
<div className="chat-input-zone">
  <div className="chat-input-icon">☷</div>

  <div className="chat-input-title">
    Paste suspicious content
  </div>

  <div className="chat-input-subtitle">
    SMS, WhatsApp messages, or call transcripts
  </div>

  <textarea
    placeholder="Paste a suspicious message or call transcript..."
    value={message}
    onChange={(e) => setMessage(e.target.value)}
  />

  <div className="character-count">
    {message.length} characters
  </div>
</div>

 <button
  onClick={async () => {
    const response = await fetch("https://kavach-te0g.onrender.com/api/analyze/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message }),
    })

   const data = await response.json()

setAnalysis(data.analysis)
  }}
>
  Scan Message
</button>
</div>
        </section>

        <section className="result-section">
  <h2>Security Analysis</h2>

  <div className="result-placeholder">
    {analysis ? (
      <>
    {analysis.decoded_data && (
  <p>
    <strong>Decoded Data:</strong>{" "}
    {analysis.decoded_data}
  </p>
)}

{analysis.package_name && (
  <p>
    <strong>Package Name:</strong>{" "}
    {analysis.package_name}
  </p>
)}

{analysis.permissions && (
  <>
    <h4>Permissions</h4>
    <ul>
      {analysis.permissions.map((permission, index) => (
        <li key={index}>{permission}</li>
      ))}
    </ul>
  </>
)}
{analysis.apk_findings && (
  <>
    <h4>Technical Findings</h4>
    <ul>
      {analysis.apk_findings.map((finding, index) => (
        <li key={index}>{finding}</li>
      ))}
    </ul>
  </>
)}
        <div className={`risk-badge ${analysis.risk_level.toLowerCase()}`}>
  ⚠ {analysis.risk_level} Risk
</div>
        <h4>Red Flags</h4>
<ul>
  {analysis.key_findings.map((finding, index) => (
    <li key={index}>{finding}</li>
  ))}
</ul>
<div className="analysis-box explanation-box">
  <h4>Explanation</h4>
  <p>{analysis.explanation}</p>
</div>

<div className="analysis-box recommendation-box">
  <h4>Recommended Action</h4>
  <p>{analysis.recommended_action}</p>
</div>
      </>
    ) : (
      <>
        <p>Your analysis result will appear here.</p>
        <span>Risk Level • Red Flags • Recommendation</span>
      </>
    )}
  </div>
</section>
      </main>
    </div>
  )
}

export default App