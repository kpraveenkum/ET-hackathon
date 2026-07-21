import { useState } from "react";

function App() {

  const [file, setFile] = useState(null);

  const [uploadInfo, setUploadInfo] = useState(null);

  const [question, setQuestion] = useState("");

  const [answer, setAnswer] = useState("");

  const [agent, setAgent] = useState("");

  const [sources, setSources] = useState([]);

  const [uploadLoading, setUploadLoading] = useState(false);

  const [chatLoading, setChatLoading] = useState(false);



  async function uploadDocument() {

    if (!file) return;

    const formData = new FormData();

    formData.append("file", file);

    setUploadLoading(true);

    setUploadInfo(null);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/upload/",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      setUploadInfo(data);

    } catch (err) {

      alert(err);

    }

    setUploadLoading(false);
  }



  async function askQuestion() {

    setChatLoading(true);

    setAnswer("");

    setAgent("");

    setSources([]);

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/chat",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            question,
          }),
        }
      );

      const data = await response.json();

      setAgent(data.agent);

      setAnswer(data.answer);

      setSources(data.sources);

    } catch (err) {

      alert(err);

    }

    setChatLoading(false);
  }



  return (

    <div style={{padding:40,fontFamily:"Arial"}}>

      <h1>AI EPC Project Intelligence Platform</h1>

      <p>
        Upload EPC Engineering Documents and ask AI questions.
      </p>

      <hr/>

      <h2>Upload Document</h2>

      <input

        type="file"

        onChange={(e)=>setFile(e.target.files[0])}

      />

      <br/><br/>

      <button

        onClick={uploadDocument}

      >

        {uploadLoading ? "Uploading..." : "Upload"}

      </button>

      <br/><br/>

      {

        uploadInfo && (

          <div
          style={{
            border:"1px solid gray",
            padding:20,
            borderRadius:10
          }}
          >

            <h3>Document Indexed Successfully</h3>

            <p><b>Filename:</b> {uploadInfo.original_filename}</p>

            <p><b>Document Type:</b> {uploadInfo.document_type}</p>

            <p><b>Discipline:</b> {uploadInfo.discipline}</p>

            <p><b>Project:</b> {uploadInfo.project}</p>

            <p><b>Pages:</b> {uploadInfo.pages}</p>

            <p><b>Chunks:</b> {uploadInfo.chunks}</p>

            <p><b>Indexed:</b> {uploadInfo.documents_added}</p>

          </div>

        )

      }

      <hr/>

      <h2>Ask AI</h2>

      <textarea

        rows={5}

        cols={70}

        value={question}

        onChange={(e)=>setQuestion(e.target.value)}

      />

      <br/><br/>

      <button

        onClick={askQuestion}

      >

        {chatLoading ? "Thinking..." : "Ask"}

      </button>

      {

        answer && (

          <div
          style={{
            marginTop:30,
            border:"1px solid gray",
            padding:20,
            borderRadius:10
          }}
          >

            <h3>Selected Agent</h3>

            <p>{agent}</p>

            <h3>Answer</h3>

            <p>{answer}</p>

            <h3>Sources</h3>

            <ul>

            {

              sources.map((s,index)=>(

                <li key={index}>
                  {s}
                </li>

              ))

            }

            </ul>

          </div>

        )

      }

    </div>

  );

}

export default App;