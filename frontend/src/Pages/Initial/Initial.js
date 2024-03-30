// import React, { useEffect } from 'react';
// import { usePorcupine } from '@picovoice/porcupine-react';

// const Initial = () => {
//     const {
//         keywordDetection,
//         isLoaded,
//         isListening,
//         error,
//         init,
//         start,
//         stop,
//         release,
//     } = usePorcupine();

//     const porcupineKeyword = { publicPath: "/HI-Aura_en_wasm_v3_0_0.ppn" };
//     const porcupineModel = { publicPath: "/procupine_params_es.pv" };

//     useEffect(() => {
//         const initializePorcupine = async () => {
//             try {
//                 await init(
//                     "W2Seq1qvSHOkrlveTuVC1ZfdjaclPsWlhm75QrRy2dF09mfj5Po4VA==",
//                     porcupineKeyword,
//                     porcupineModel
//                 );
//             } catch (e) {
//                 console.error("Error initializing Porcupine:", e);
//             }
//         };

//         initializePorcupine();
//     }, [init, porcupineKeyword, porcupineModel]);

//     const handleStart = () => {
//         if (isLoaded) {
//             console.log("listening...");

//             start();
//             console.log("Started listening...");
//         }
//     };

//     return (
//         <div style={{ position: 'relative', backgroundColor: 'white', height:'100vh' }}>
//             <button onClick={handleStart}>Start Listening</button>
//             {isLoaded ? (
//                 <div>
//                     {/* Your content when Porcupine is loaded */}
//                 </div>
//             ) : (
//                 <div>Loading Porcupine...</div>
//             )}
//         </div>
//     );
// };

// export default Initial;

import React, { useEffect } from 'react';
import { BuiltInKeyword } from '@picovoice/porcupine-web';
import { usePorcupine } from '@picovoice/porcupine-react';
import porcupineModel from '../../components/model.pv' 

const Initial = () => {
  const {
    keywordDetection,
    isLoaded,
    isListening,
    error,
    init,
    start,
    stop,
    release,
  } = usePorcupine();

  useEffect(() => {
    const initializePorcupine = async () => {
      try {
        await init(
            'W2Seq1qvSHOkrlveTuVC1ZfdjaclPsWlhm75QrRy2dF09mfj5Po4VA==',
          [BuiltInKeyword.Porcupine],
          porcupineModel
        );
      } catch (e) {
        console.error("Error initializing Porcupine:", e);
      }
    };

    initializePorcupine();
  }, [init]);

  useEffect(() => {
    if (keywordDetection !== null) {
      console.log(keywordDetection.label);
    }
  }, [keywordDetection]);

  const handleStart = async () => {
    try {
      await start();
    } catch (e) {
      console.error("Error starting Porcupine:", e);
    }
  };

  const handleStop = async () => {
    try {
      await stop();
    } catch (e) {
      console.error("Error stopping Porcupine:", e);
    }
  };

  const handleRelease = async () => {
    try {
      await release();
    } catch (e) {
      console.error("Error releasing Porcupine resources:", e);
    }
  };

  return (
    <div>
      <h1>Porcupine Wake Word Detection</h1>
      <p>Picovoice Porcupine is {isLoaded ? 'loaded' : 'loading'}.</p>
      <p>Listening: {isListening ? 'Yes' : 'No'}</p>
      {error && <p>Error: {error.message}</p>}
      <button onClick={handleStart} disabled={!isLoaded || isListening}>Start</button>
      <button onClick={handleStop} disabled={!isListening}>Stop</button>
      <button onClick={handleRelease} disabled={!isLoaded || isListening}>Release</button>
    </div>
  );
};

export default Initial;
