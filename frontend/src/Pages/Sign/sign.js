import {React,useState,useEffect} from 'react'
import Paper from '@mui/material/Paper';
import { Box } from '@mui/system';
import './sign.css'
import { TextField, Typography } from '@mui/material';
import { Button } from '@mui/base';
import { Link ,useNavigate} from 'react-router-dom';
// import Particle from '../../Components/Particle';
import Swal from 'sweetalert2'
import axios from 'axios';
import './sign.css'
import Spline from '@splinetool/react-spline';
import { GoogleLogin } from '@react-oauth/google';
// import GoogleLogin from 'react-google-login';
// import { useNavigate } from 'react-router-dom';
import { googleLogout, useGoogleLogin } from '@react-oauth/google';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme({
    components: {
      MuiInputBase: {
        styleOverrides: {
          input: {
            '&::placeholder': {
              color: 'white', // Change the color here
            },
          },
        },
      },
    },
  });

const Sign = () => {
    // const navigate= useNavigate();
    const [name , setName] = useState('');
    const [location , setLocation] = useState('');
    const [email , setEmail] = useState('');
    const [password, setPassword] = useState('');
    const navigate = useNavigate();


    const [ user, setUser ] = useState([]);
    const [ profile, setProfile ] = useState([]);

    const login = useGoogleLogin({
        onSuccess: (codeResponse) => setUser(codeResponse),
        onError: (error) => console.log('Login Failed:', error)
    });

    useEffect(
        () => {
            if (user) {
                axios
                    .get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${user.access_token}`, {
                        headers: {
                            Authorization: `Bearer ${user.access_token}`,
                            Accept: 'application/json'
                        }
                    })
                    .then((res) => {
                        setProfile(res.data);
                        navigate('/recorder')
                    })
                    .catch((err) => console.log(err));
            }
        },
        [ user ]
    );

    console.log(profile)
    const handleRegister = async() =>{
        try{
            if(!email||!password||!name||!location){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please Fill All fields',
                })
            }else{
                // const response = await axios.post("http://localhost:8000/user/register",{
                //     name,
                //     location,
                //     email,
                //     password
                // });
                // if(response.status == 201){
                //     setTimeout(() => {
                //         navigate('/voice-initial')  
                //     }, 1500);
                    navigate('/recorder')
                    Swal.fire(
                        'YAYY!',
                        'Successful Registration',
                        'success'
                    )
                //     }
                // else{
                //     Swal.fire({
                //         icon: 'error',
                //         title: 'Oops...',
                //         text: 'Something went wrong!',
                //     })
                // }
            }
        }catch(err){
            console.log(err);
            if(err.response.data.message.includes('Email is already in use!!')){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Email already in use :(',
                })
            }
            else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Something went wrong!',
                })
            }
        }
    }

  return (
    <div style={{ position: 'relative', backgroundColor: 'black', height:'100vh' }}>
    <Box style={{ zIndex: 0, position: 'relative' }}>
        <Spline scene="https://prod.spline.design/abI9MJcWPEXkLkxT/scene.splinecode" className='animation' />
    </Box>

    <Box style={{ zIndex: 1, position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }} className='gradient' sx={{
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        margin: '1em',
        
    }}>
        <Paper elevation={3} className='paper-sign' style={{ zIndex: 1, position: 'relative', marginTop:'10em' }}>
            <Box style={{ zIndex: 1, position: 'relative' }}>
                <Box display="flex" flexDirection="column" alignItems="center" >
                    <Typography variant='h3'  style={{
                        alignSelf: 'center',
                        fontWeight: 'bolder',
                        color: 'white',
                        fontSize:'1.5em'
                    
                    }}>
                        Sign Up
                    </Typography>
                </Box>
                <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    fontSize:'1em'
                }}>
                Name:
                </Typography>
                <TextField fullWidth className='text-field' InputProps={{ style: { color: 'white' } }}  onChange={e => setName(e.target.value)}  size='small'/>
                <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    fontSize:'1em'

                }}>
                    Location:
                </Typography>
                <TextField fullWidth className='text-field'InputProps={{ style: { color: 'white' } }}  onChange={e => setLocation(e.target.value)} size='small' />
                <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    fontSize:'1em'

                }}>
                    Email:
                </Typography>
                <TextField fullWidth className='text-field' InputProps={{ style: { color: 'white' } }}  onChange={e => setEmail(e.target.value)} size='small'/>
                <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    fontSize:'1em'

                }}>
                    Password:
                </Typography>
                <TextField fullWidth className='text-field' InputProps={{ style: { color: 'white' } }}  onChange={e => setPassword(e.target.value)} size='small' />

                <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    marginLeft:'50%',
                    marginRight: 'auto',
                    fontSize:'1em'


                }}>
                    OR
                </Typography>
                <Box display='flex' flexDirection='column' alignItems='center'>
    <Button className='google' fullWidth onClick={login} style={{ display: 'flex', alignItems: 'center' }}>
        <img src="https://developers.google.com/identity/images/g-logo.png" alt="Google Logo" style={{ width: '30px', height: '30px', marginRight:'18%', marginLeft: '20px' }} />
        <span >Sign Up with Google</span>
    </Button>
</Box>

                <Box display='flex' flexDirection='column' alignItems='center'>
                    <Button className='button-sign-up' fullWidth onClick={handleRegister}>
                        Sign Up
                    </Button>
                </Box>
            </Box>
        </Paper>
    </Box>
</div>

  )
}

export default Sign