import React, { useState, useEffect, useRef } from 'react';
import { Porcupine, PorcupineEngine } from '@picovoice/porcupine-web';
import { Recorder } from '@picovoice/web-voice-processor';

const WakeWordDetector = ({ wakeWord, onWakeWordDetected }) => {
  const accessKey = 'WscJfSbrbDqIoMsfY9VvyLLfdAmjFwyzeZ8FiCuMuitH25m6YYjzmA=='; // Replace with your Picovoice Access Key
  const [isListening, setIsListening] = useState(false);
  const recorderRef = useRef(null);
  const porcupineRef = useRef(null);

  useEffect(() => {
    const startListening = async () => {
      console.log("Start listening called");
      if (!recorderRef.current || !porcupineRef.current) {
        return;
      }
  
      try {
        console.log("Listening started");
        const wakeWordPath = 'C:/Users/aasmi/Desktop/codeshastra/Codeshastra_Tensionflow/hack/public/HI-Aura_en_wasm_v3_0_0.ppn';
        await porcupineRef.current.initialize({
          accessKey,
          keywordPaths: [wakeWord], // Path to your .ppn file (if custom)
        });
        await recorderRef.current.start();
        setIsListening(true);
      } catch (error) {
        console.error('Porcupine initialization error:', error);
      }
    };
  
    const stopListening = async () => {
      console.log("Stop listening called");
      if (!recorderRef.current || !porcupineRef.current) {
        return;
      }
  
      try {
        console.log("Listening stopped");
        await recorderRef.current.stop();
        await porcupineRef.current.delete();
        setIsListening(false);
      } catch (error) {
        console.error('Porcupine cleanup error:', error);
      }
    };
  
    if (isListening) {
      startListening();
    } else {
      // No need to call stopListening here
    }
  
    return () => {
      // Cleanup function for useEffect
      stopListening(); // Call stopListening only when the component unmounts
    };
  }, [isListening, wakeWord]); // Re-run on wakeWord change
    
  const handleAudioFrame = async (audioFrame) => {
    if (!porcupineRef.current) {
      return;
    }

    try {
      const keywordIndex = await porcupineRef.current.process(audioFrame);
      if (keywordIndex !== -1) {
        onWakeWordDetected(); // Call your callback here
      }
    } catch (error) {
      console.error('Porcupine audio processing error:', error);
    }
  };

  return (
    <div>
      <button onClick={() => setIsListening(!isListening)}>
        {isListening ? 'Stop Listening' : 'Start Listening'}
      </button>
    </div>
  );
};

export default WakeWordDetector;