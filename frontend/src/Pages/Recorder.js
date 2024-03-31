import React from 'react';
import { useState,useRef, useEffect } from 'react'
import Spline from '@splinetool/react-spline';
import { TextField, Typography } from '@mui/material';
import { Box } from '@mui/material';
import './Recorder.css'
import { Button } from '@mui/base';
import Paper from '@mui/material/Paper';
import '../Pages/Dashboard/Dashboard.css'
import Swal from 'sweetalert2'
import { Link } from 'react-router-dom';
import { useNavigate } from 'react-router-dom';


import { ReactMic } from 'react-mic';

export default function App() {
    const [voiceOn, setVoiceOn] = useState(true);
    const [isRecording, setIsRecording] = useState(false);

    const navigate = useNavigate();

    const handleNavigateToDashboard = () => {
      navigate('/dashboard');
    };

    const startRecording = () => {
        setIsRecording(true);
    };

    const stopRecording = () => {
        setIsRecording(false);
    };

    const onStop = (recordedBlob) => {
        console.log('Recording stopped:', recordedBlob);
        Swal.fire(
            'YAYY!',
            'Successful Voice Recording',
            'success'
        )
        
    };

    const toggleMicrophone = () => {
        setVoiceOn(prevState => !prevState);
        if (voiceOn == true)
        {
            startRecording()
           

        }
        else
        {
            stopRecording()
            
        }

    };





  return (
    <div style={{ position: 'relative', backgroundColor: 'black', height:'100vh' }}>
            <Box style={{ zIndex: 0, position: 'relative' }}>
        <Spline scene="https://prod.spline.design/DmMr7ty3vpbu1HWs/scene.splinecode" className='animation' />
    </Box>

            <Box style={{ zIndex: 1, position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }} className='gradient' sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        margin: '1em',
    }}>

<ReactMic 
            record={isRecording}
            // className="sound-wave"
            onStop={onStop}
            // onData={onData}
            strokeColor="purple"
            backgroundColor='black'
            className ='line'
            
            />

                <Paper elevation={3} className='paper' style={{ zIndex: 1, position: 'relative' }} >
                    <Box  >
                        <Box display="flex" flexDirection="column" alignItems="center">
                            <Typography variant='h3' style={{
                                alignSelf: 'center',
                                // fontStyle:'italic',
                                fontWeight: 'bolder',
                                color: 'white'
                            }}>
                                Getting Started
                            </Typography>
                        </Box>
                        <Box display="flex" flexDirection="column" alignItems="center">
                        <Typography variant='h6' sx={{
                            marginTop: '1em',
                            fontWeight: '600',
                            color: 'white',
                            marginBottom:'1em',
                           

                        }}>
                            Input a voice audio file
                        </Typography>
                        </Box>
                        <input type="file" name="file" id="file" style={{marginLeft:'7.5em'}} />
                        
                       
                        
                        <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    marginLeft:'45%',
                    marginRight: 'auto'

                }}>
                    OR
                </Typography>

                <Button sx={{ backgroundColor: 'white' }} className='record' onClick={toggleMicrophone}>
      {voiceOn ? "Start Recording" : "Stop recording"}
    </Button>
                    <Button sx={{backgroundColor:'white'}} className='submit' onClick={handleNavigateToDashboard}> Submit </Button>
               

                    </Box>
                </Paper>
            </Box>

            {/* <Box className='particle'> */}

            {/* </Box> */}
        </div>
  );
}
