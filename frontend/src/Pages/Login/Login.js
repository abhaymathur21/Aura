// import React from 'react'
import { React, useState,useEffect } from 'react'
import Paper from '@mui/material/Paper';
import { Box } from '@mui/system';
import './login.css'
import { TextField, Typography } from '@mui/material';
import { Button } from '@mui/base';
import { Link } from 'react-router-dom';
// import Particle from '../../Components/Particle';
// import Login2 from './Login2';
// import { Button } from 'flowbite-react';
import { useNavigate } from 'react-router-dom';
import Swal from 'sweetalert2'
import axios from 'axios';

import Spline from '@splinetool/react-spline';

import { googleLogout, useGoogleLogin } from '@react-oauth/google';


const Login = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const [ user, setUser ] = useState([]);
    const [ profile, setProfile ] = useState([]);


    const login = 
    useGoogleLogin({
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
                        navigate('/')
                    })
                    .catch((err) => console.log(err));
            }
        },
        [ user ]
    );


    const handleLogin = async ()=>{
        try{
            if(!email||!password){
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: 'Please Fill All fields',
                })
            }else{
                const response = await axios.post("http://localhost:8000/user/login",{
                    email,
                    password
                });
                localStorage.setItem("token",response.data.token)
                if(response.status == 200){
                    navigate('/lawyers')  
                }
                else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: 'Invalid Login Credentials',
                    })
                }
            }
        }catch(err){
            console.log(err)
            Swal.fire({
                icon: 'error',
                title: 'Oops...',
                text: 'Invalid Login Credentials',
            })
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

                <Paper elevation={3} className='paper' style={{ zIndex: 1, position: 'relative' }} >
                    <Box  >
                        <Box display="flex" flexDirection="column" alignItems="center">
                            <Typography variant='h3' style={{
                                alignSelf: 'center',
                                // fontStyle:'italic',
                                fontWeight: 'bolder',
                                color: 'white'
                            }}>
                                Login
                            </Typography>
                        </Box>
                        <Typography variant='h6' sx={{
                            marginTop: '1em',
                            fontWeight: '600',
                            color: 'white'

                        }}>
                            email:
                        </Typography>
                        <TextField fullWidth className='text-field' onChange={(e)=>setEmail(e.target.value)}>
                        </TextField>
                        <Typography variant='h6' sx={{
                            marginTop: '1em',
                            fontWeight: '600',
                            color: 'white'


                        }}>
                            password:
                        </Typography>
                        <TextField fullWidth className='text-field' onChange={(e)=>setPassword(e.target.value)}>
                        </TextField>
                        <Typography variant='h6' sx={{
                    marginTop: '1em',
                    fontWeight: '600',
                    color:'white',
                    marginLeft:'50%',
                    marginRight: 'auto'

                }}>
                    OR
                </Typography>
                <Button onClick={login} className='google'>Log in with Google</Button>
                        <Box display='flex' flexDirection='column' alignItems='center' >
                            <Button className='button-login' fullWidth onClick={handleLogin}>
                                Login
                            </Button>
                            <Typography style={{
                                fontSize: '15px',
                                marginTop: '1em',
                                fontWeight: 'bold',
                            color: 'white'
                                

                            }}>
                                Not registered ? <Link to='/sign-up' className='link-sign' > <u>Sign up</u></Link>

                            </Typography>
                        </Box>


                    </Box>
                </Paper>
            </Box>

            {/* <Box className='particle'> */}

            {/* </Box> */}
        </div>

    )
}

export default Login


