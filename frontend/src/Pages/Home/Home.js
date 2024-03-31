import React from 'react'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography'
import Button from '@mui/material/Button';
import Spline from '@splinetool/react-spline';
import Nav from '../../components/Nav';
import Typewriter from 'typewriter-effect';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import './Home.css'



const Home = () => {
  return (
<Box sx={{backgroundColor:'black'}}>
    <Nav/>
    <Spline scene="https://prod.spline.design/ZrTWz0FeJ0cBpnLO/scene.splinecode" className='animation' />
    <Box className='typewriter'>
    <Typewriter
        options={{
          strings: ['Where <span style="font-style:italic">AI</span> meets Innovation .'],
          autoStart: true,
          loop: false,
          wrapperClassName: 'typewriter-text',
          cursorClassName: 'typewriter-cursor',
        }}
        onInit={(typewriter) => {
          typewriter.typeString('Where <span style="font-style:italic">AI</span> meets Innovation .')
            .callFunction(() => {
              console.log('String typed out!');
            })
            .start();
        }}
      /><Box  sx={{ marginTop: '1rem' }}>
          <Button className='signup' variant="contained" color="primary" endIcon={<ArrowForwardIcon />}>
            Sign Up
          </Button>
        </Box>
    </Box>
    
</Box>
  )
}

export default Home
