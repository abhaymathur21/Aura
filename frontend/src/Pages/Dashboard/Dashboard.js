import { useState, useRef, useEffect } from "react";
import React from "react";
import NavDash from "../../components/NavDash";
import { Box, Grid, Button, Typography } from "@mui/material";
import "./Dashboard.css";
import { cva } from "class-variance-authority";
import TextField from "@mui/material/TextField";
// import { Button } from 'flowbite-react'
import KeyboardVoiceIcon from "@mui/icons-material/KeyboardVoice";
import FileUploadIcon from "@mui/icons-material/FileUpload";

import Modal from '@mui/material/Modal';
import { MuiFileInput } from 'mui-file-input'
import { createTheme, ThemeProvider } from '@mui/material/styles';

import Autocomplete from '@mui/material/Autocomplete'

import AccountCircleIcon from "@mui/icons-material/AccountCircle";
import axios from "axios";

import MicOffIcon from "@mui/icons-material/MicOff";

import { ReactMic } from "react-mic";

import SpeechRecognition, {
  useSpeechRecognition,
} from "react-speech-recognition";

const theme = createTheme({
  components: {
    MuiInputBase: {
      styleOverrides: {
        input: {
          "&::placeholder": {
            color: "white", // Change the color here
          },
        },
      },
    },
  },
});
const style = {
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  width: 400,
  bgcolor: "background.paper",
  border: "2px solid #000",
  borderRadius: "5px",
  boxShadow: 24,
  p: 4,
};

const Dashboard = () => {
  const [messages, setMessages] = useState([
    { user: "agent", message: "Hi there! How can I help you today?" },
  ]);
  const [ResponseButton, SetResponseButton] = useState([]);

  const [input, setInput] = useState("");

      const [voiceOn, setVoiceOn] = useState(true);
      const [isRecording, setIsRecording] = useState(false);

      const [inputValue, setInputValue] = useState('');
      const [options, setOptions] = useState([]);


      useEffect(() => {
        // Function to play speech for the last message
        const playSpeechForLastMessage = () => {
          
          const lastMessage = messages[messages.length - 1];
          if (lastMessage && lastMessage.user == 'agent') {
            // Use speech synthesis API to speak the last message
            const speechSynthesisUtterance = new SpeechSynthesisUtterance(lastMessage.message);
            window.speechSynthesis.speak(speechSynthesisUtterance);
          }
        };

        playSpeechForLastMessage();

        // Clean-up function
        return () => {
          // Stop speech synthesis when component unmounts
          window.speechSynthesis.cancel();
        };
      }, [messages]);
      
      useEffect(() => {
        const fetchAutocompleteOptions = async () => {
          try {
            console.log("yo")
            const response = await axios.get('https://omrivolk-autocomplete-v1.p.rapidapi.com/complete', {
              params: { s: input },
              headers: {
                'X-RapidAPI-Key': 'cc9c33e7d9mshf2ba8d9b84a6782p1b309ejsn389c10a0b6a1',
                'X-RapidAPI-Host': 'omrivolk-autocomplete-v1.p.rapidapi.com'
              }
            });
            setOptions(response.data);
            console.log("Got the dataa")
            console.log(response.data)
          } catch (error) {
            console.error(error);
          }
        };
    
        if (input.trim() !== '') {
          fetchAutocompleteOptions();
        } else {
          setOptions([]);
        }
      }, [input]);

    
    const domainFileRef = useRef(null);


    const chatVariant = cva("p-2 text-pretty flex", {
        variants: {
            variant: {
                user: "bg-white text-primary rounded-br-none ml-[100] ",
                agent: "bg-purple-500 text-white rounded-bl-none mr-auto",
            },
        },
    });
  

    const handleSubmit = () =>
    {
        console.log('started submitting')
        if(domainFileRef !== null && domainFileRef.current.files.length > 0)
        {
            console.log(domainFileRef?.current?.files?.[0]);

            var formData = new FormData();
            formData.append('file', domainFileRef?.current?.files?.[0]);
            formData.append('message', input);
      // console.log(formData)
      formData.forEach((value, key) => {
        console.log("Hi")
        console.log(key + ":" + value);
      });

      setInput("")

      axios
        .post(
          "http://127.0.0.1:5000/upload_file",
          formData,
          {
            headers: {
              "Content-Type": "multipart/form-data",
            },
          }
        )
        .then((res) => {
          console.log("response File", res.data.data);
          setInput("")
          setMessages((prevMessages) => [
            ...prevMessages,
            { user: "agent", message: res.data.data},
          ]);
        })
        .catch((err) => {
          console.log(err);
        });
    }
    if (input == "" && transcript) {
      input = transcript;
    }

    if (input != "") {
      console.log("sending message");
      setMessages((prevMessages) => [
        ...prevMessages,
        { user: "user", message: input },
      ]);
      axios
        .post(
          "http://127.0.0.1:5000/llm_chatbot/1",
          {
            message: input,
          },
          {
            headers: {
              "Content-Type": "application/json",
            },
          }
        )
        .then((res) => {
          console.log("response Text", res.data);

          setMessages((prevMessages) => [
            ...prevMessages,
            { user: "agent", message: res.data.data },
          ]);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };

  const handleInput = (event) => {
    setInput(event.target.value);

    console.log(input);
  };

  useEffect(() => {
    axios
      .post(
        "http://127.0.0.1:5000/update_person/1",
        {
          messages: messages,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      )
      .then((res) => {
        console.log("Done sent chat history");
      })
      .catch((err) => {
        console.log(err);
      });
  }, [messages]);

  const startRecording = () => {
    setIsRecording(true);
  };

  const stopRecording = () => {
    setIsRecording(false);
  };

  const onStop = (recordedBlob) => {
    console.log("Recording stopped:", recordedBlob);

    // Create a new FormData object
    const formData = new FormData();

    // Append the recordedBlob to the FormData object
    formData.append("audio", recordedBlob.blob, "audio.wav");

    axios
      .post(
        "http://127.0.0.1:5000/audio",
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        }
      )
      .then(() => {
        console.log("sent Audio successfully");
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const {
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition,
    startListening,
    stopListening,
  } = useSpeechRecognition();

  const toggleMicrophone = () => {
    setVoiceOn((prevState) => !prevState);
    if (voiceOn == true) {
      startRecording();
      SpeechRecognition.startListening();
    } else {
      stopRecording();
      SpeechRecognition.stopListening();
    }
  };

  if (!browserSupportsSpeechRecognition) {
    return <span>Browser doesn't support speech recognition.</span>;
  }
  let ResponseButtonData = [];

      if (Object.keys(ResponseButton).length !== 0) {
          ResponseButtonData = Object.keys(ResponseButton).map((key) => ({
              label: ResponseButton[key],
              taskId: key,
          }));
      }




  

    

  return (
    <>
      <Box
        sx={{
          backgroundColor: "black",
          minHeight: "100vh",
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* // Conditionally render the <ReactMic> component if voiceOn is true */}

        <ReactMic
          record={isRecording}
          // className="sound-wave"
          onStop={onStop}
          // onData={onData}
          strokeColor="purple"
          backgroundColor="black"
          className="line"
        />

        <NavDash />
        {/* <p style={{color:'white'}}>{transcript}</p> */}

        <Box sx={{ flex: "1 0 auto", overflowY: "auto" }}>
          <Box className="scrollable-div">
            {messages.map((message, index) => (
              
                <Typography
                  key={index}
                  sx={{
                    width: "30vw",
                    marginLeft: message.user === "user" ? "auto" : "initial",
                    borderRadius: "10px",
                    marginBottom: "10px",
                  }}
                  className={chatVariant({ variant: message.user })}
                >
                  {typeof message.message === 'object' ? JSON.stringify(message.message) : message.message}
                </Typography>
              
            ))}
          </Box>
        </Box>
        <Box className="footer" sx={{ flexShrink: 0 }}>
          <Grid container>
            <Grid item xs={1} />
            <Grid item xs={3}>
              <input type="file" name="file" id="file" ref={domainFileRef} />
            </Grid>
            <Grid item xs={4}>
            <ThemeProvider theme={theme}>
            <TextField
            id="chat"
            placeholder='Ask a Question ...'
            name='chat'
            value={input||transcript}
            onChange = {handleInput}
            className='search'
            fullWidth
            InputProps={{ style: { color: 'white' } }}
            
            />

{/* <Autocomplete
  disablePortal
  id="combo-box-demo"
  options={options}
  sx={{ width: 300 }}
  renderInput={(params) => (
    <TextField
      {...params}
      id="chat"
      placeholder='Ask a Question ...'
      name='chat'
      value={input || transcript}
      onChange={handleInput}
      className='search'
      fullWidth
      InputProps={{ style: { color: 'white' } }}
    />
  )}
/> */}


            </ThemeProvider>
            
            </Grid>

            <Grid item xs={1}>
              <Button className="dash-button" onClick={toggleMicrophone}>
                {voiceOn ? (
                  <KeyboardVoiceIcon color="white" fontSize="large" />
                ) : (
                  <MicOffIcon color="white" fontSize="large" />
                )}
              </Button>
            </Grid>
            <Grid item xs={2}>
              <Button fullWidth className="dash-button" onClick={handleSubmit}>
                Submit
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </>
  );
};

export default Dashboard;
