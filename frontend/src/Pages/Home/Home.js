import React from 'react'
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography'
import Spline from '@splinetool/react-spline';
import Nav from '../../components/Nav';
import Typewriter from 'typewriter-effect';
import './Home.css'

const Home = () => {
  return (
<Box sx={{backgroundColor:'black'}}>
    <Nav/>
    <Spline scene="https://prod.spline.design/Clu6hKdXDJQJ8YvL/scene.splinecode" className='animation' />
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
      />
    </Box>
    
</Box>
  )
}

export default Home
