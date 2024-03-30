import logo from './logo.svg';
import './App.css';
import Spline from '@splinetool/react-spline';
import Nav from './components/Nav.js'

import x from './logo.png'
import Home from './Pages/Home/Home.js';
import Sign from './Pages/Sign/sign';
import { Route,Routes, BrowserRouter } from 'react-router-dom';
import Login from './Pages/Login/Login';
import Initial from './Pages/Initial/Initial';
import WakeWordDetector from './Pages/Initial/Initial2';
import Dashboard from './Pages/Dashboard/Dashboard.js';
import Profile from './Pages/Profile/Profile.js';




function App() {
  const handleWakeWord = () => 
  {
    console.log("detected")
  }

  return (

    <BrowserRouter>
      <Routes>
        <Route path='/' element={<Home/>}></Route>
        <Route path='/signup' element={<Sign/>}></Route>
        <Route path='/login' element={<Login/>}/>
        <Route path='/initial' element={<Initial/>}/>
        <Route path='/dashboard' element={<Dashboard/>}/>
        <Route path='/profile' element={<Profile/>}/>
        


        
      </Routes>
    </BrowserRouter>
    
    // <WakeWordDetector wakeWord="C:/Users/aasmi/Desktop/codeshastra/Codeshastra_Tensionflow/hack/public/HI-Aura_en_wasm_v3_0_0.ppn" onWakeWordDetected={handleWakeWord}/>

    
    


  );
}

export default App;
