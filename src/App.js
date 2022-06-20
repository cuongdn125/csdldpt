import axios from "axios";
import { useState } from "react";
import "./App.css";

function App() {
  const [selectFile, setSelectFile] = useState("");
  const [fileInputState, setFileInputState] = useState("");
  const [previewFileSource, setPreviewSource] = useState("");
  const [classification, setClassification] = useState("");

  const handleFileInputChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      previewFile(file);
      setSelectFile(file);
      setFileInputState(e.target.value);
    }
  };
  const previewFile = (file) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onloadend = () => {
      setPreviewSource(reader.result);
    };
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (selectFile) {
      const reader = new FileReader();
      reader.readAsDataURL(selectFile);
      reader.onload = async () => {
        await axios
          .post("http://127.0.0.1:5000", {
            content: reader.result,
          })
          .then((res) => {
            console.log(res);
            setClassification(res.data.class);
          })
          .catch((err) => {
            console.log(err);
          });
      };
      reader.onerror = () => {
        console.error("AHHHHHHHH!!");
        // setErrMsg("something went wrong!");
      };
    }
  };

  return (
    <div style={styles.container}>
      <input accept="image/*" type="file" onChange={handleFileInputChange} />

      {selectFile && (
        <div style={styles.preview}>
          <img src={previewFileSource} style={styles.image} alt="Thumb" />
          <button onClick={handleSubmit} style={styles.delete}>
            Submit Image
          </button>
        </div>
      )}

      {classification && (
        <div style={styles.classification}>
          <h1>{classification}</h1>
        </div>
      )}
    </div>
  );
}
const styles = {
  container: {
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    alignItems: "center",
    paddingTop: 50,
  },
  preview: {
    marginTop: 50,
    display: "flex",
    flexDirection: "column",
  },
  image: { maxWidth: "100%", maxHeight: 320 },
  delete: {
    cursor: "pointer",
    padding: 15,
    background: "red",
    color: "white",
    border: "none",
  },
};

export default App;
