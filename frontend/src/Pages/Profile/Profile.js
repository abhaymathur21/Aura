import React from 'react'
import NavDash from '../../components/NavDash'
import { Box, Typography,Button } from '@mui/material'
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import ArrowCircleRightIcon from "@mui/icons-material/ArrowCircleRight";
import LocationOnIcon from '@mui/icons-material/LocationOn';
import Spline from '@splinetool/react-spline';
import './Profile.css'
import DeleteIcon from '@mui/icons-material/Delete';
import ModeEditIcon from '@mui/icons-material/ModeEdit';
import ArrowBackIosNewIcon from '@mui/icons-material/ArrowBackIosNew';
import { useNavigate } from 'react-router-dom';
import NavOut from '../../components/NavOut';



const txtStyle = {
    //  fontFamily: 'Montserrat',
    fontFamily: "sans-serif",
    fontStyle: "normal",
    // fontWeight: 700,
    fontSize: "30px",
    lineHeight: "35px",
    display: "flex",
    alignItems: "center",
    // textAlign: "center",
    color:"white"
  };
const Profile = () => {
  const navigate = useNavigate();
  const handleFile = () =>
  {
    navigate('/dashboard')
  }
  return (
    
    <Box sx={{backgroundColor:'black', minHeight: '100vh' , height:'auto'}}>
        <Box style={{ zIndex: 0, position: 'relative' }}>
        <Spline scene="https://prod.spline.design/abI9MJcWPEXkLkxT/scene.splinecode" className='animation' />
        </Box>
        <Box style={{ zIndex: 1, position: 'absolute', top: 0, left: 0, right: 0, bottom: 0 }}>
        <NavOut/>
        <Box sx={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center', marginTop:'1em'}}>
                  <Button
                    size="40rem"
                    sx={{color:'white',marginRight: 'auto', marginLeft:'3em'}}
                    onClick={handleFile}
                  >
                    <ArrowBackIosNewIcon color='white' fontSize='large'/>
                  </Button>
            <Typography variant='h4' sx={{color:'white',marginBottom:'1em'}}>Your <span>Profile</span></Typography>

            <Card
                // key={data.id}
                sx={{
                  width: "80%",
                  display: "flex",
                  position: "relative",
                  flexDirection: "row",
                  justifyContent: "space-between",
                  variant: "outlined",
                  borderRadius: "10px",
                  border: "2px solid #DEDEDE",
                  boxShadow: "none",
                  // margin: "0.8rem",
                  marginTop: "0.8rem",
                  height:'10em',
                  padding:'1.4em'
                }}
                className="Card"
                // onClick={()=>{navigate('/class')}}
                // onClick={() => {
                //   //   setSelectedNews(data);
                //   setSelectedLecture(data);
                //   console.log(data);
                //   navigate(`/class/${data.id}`);
                //   // console.log(data);
                // }}
              >
                <CardContent>
                    <Box sx={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
                    <Box >
                    <Typography
                      gutterBottom
                      variant="h5"
                      component="div"
                      style={txtStyle}
                      sx={{ fontWeight: 450 }}
                      className="Heading"
                    >
                      Aasmi Thadhani 
                      {/* {data.subject.name} */}
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      display: "flex",
                      flexDirection: "row",
                      marginBottom: "2px",
                    }}
                    className="Detail"
                  >
                   {/* <LocationOnIcon color='white' fontSize='large'/> */}
                    <Typography
                      variant="body2"
                      color="white"
                      fontSize={"17px"}
                    >
                      Mumbai
                    </Typography>
                  </Box>
                    </Box>
                  
                  
                </CardContent>
                <CardActions sx={{ float: "right" }}>
                <Button
                    size="40rem"
                    sx={{color:'white'}}
                    // onClick={() => {
                    //   //   setSelectedNews(data);
                    //   setSelectedLecture(data);
                    //   localStorage.setItem(
                    //     "LectureLocalStorage",
                    //     JSON.stringify(data)
                    //   );
                    //   navigate(`/class/${data.id}`);
                    //   // localStorage.setItem("classId", data.id);
                    //   // console.log(data);
                    // }}
                  >
                    <ModeEditIcon color='white' fontSize='large'/>
                  </Button>
                  <Button
                    size="40rem"
                    sx={{color:'white'}}
                    // onClick={() => {
                    //   //   setSelectedNews(data);
                    //   setSelectedLecture(data);
                    //   localStorage.setItem(
                    //     "LectureLocalStorage",
                    //     JSON.stringify(data)
                    //   );
                    //   navigate(`/class/${data.id}`);
                    //   // localStorage.setItem("classId", data.id);
                    //   // console.log(data);
                    // }}
                  >
                    <DeleteIcon color='white' fontSize='large'/>
                  </Button>
                </CardActions>
              </Card>










              <Card
                // key={data.id}
                sx={{
                  width: "80%",
                  display: "flex",
                  position: "relative",
                  flexDirection: "row",
                  justifyContent: "space-between",
                  variant: "outlined",
                  borderRadius: "10px",
                  border: "2px solid #DEDEDE",
                  boxShadow: "none",
                  // margin: "0.8rem",
                  marginTop: "0.8rem",
                  height:'10em',
                  padding:'1.4em'
                }}
                className="Card"
                // onClick={()=>{navigate('/class')}}
                // onClick={() => {
                //   //   setSelectedNews(data);
                //   setSelectedLecture(data);
                //   console.log(data);
                //   navigate(`/class/${data.id}`);
                //   // console.log(data);
                // }}
              >
                <CardContent>
                    <Box sx={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
                    <Box >
                    <Typography
                      gutterBottom
                      variant="h5"
                      component="div"
                      style={txtStyle}
                      sx={{ fontWeight: 450 }}
                      className="Heading"
                    >
                      Abhay Mathur
                      {/* {data.subject.name} */}
                    </Typography>
                  </Box>
                  <Box
                    sx={{
                      display: "flex",
                      flexDirection: "row",
                      marginBottom: "2px",
                    }}
                    className="Detail"
                  >
                   
                    <Typography
                      variant="body2"
                      color="white"
                     

                      fontSize={"17px"}
                    >
                      Delhi
                    </Typography>
                  </Box>
                    </Box>
                  
                  
                </CardContent>
                <CardActions sx={{ float: "right" }}>
                <Button
                    size="40rem"
                    sx={{color:'white'}}
                    // onClick={() => {
                    //   //   setSelectedNews(data);
                    //   setSelectedLecture(data);
                    //   localStorage.setItem(
                    //     "LectureLocalStorage",
                    //     JSON.stringify(data)
                    //   );
                    //   navigate(`/class/${data.id}`);
                    //   // localStorage.setItem("classId", data.id);
                    //   // console.log(data);
                    // }}
                  >
                    <ModeEditIcon color='white' fontSize='large'/>
                  </Button>
                <Button
                    size="40rem"
                    sx={{color:'white'}}
                    // onClick={() => {
                    //   //   setSelectedNews(data);
                    //   setSelectedLecture(data);
                    //   localStorage.setItem(
                    //     "LectureLocalStorage",
                    //     JSON.stringify(data)
                    //   );
                    //   navigate(`/class/${data.id}`);
                    //   // localStorage.setItem("classId", data.id);
                    //   // console.log(data);
                    // }}
                  >
                    <DeleteIcon color='white' fontSize='large'/>
                  </Button>
                </CardActions>
              </Card>







              <Card
                // key={data.id}
                sx={{
                  width: "80%",
                  display: "flex",
                  position: "relative",
                  flexDirection: "row",
                  justifyContent: "space-between",
                  variant: "outlined",
                  borderRadius: "10px",
                  border: "2px solid #DEDEDE",
                  boxShadow: "none",
                  // margin: "0.8rem",
                  marginTop: "0.8rem",
                  height:'10em',
                  padding:'1.4em'
                }}
                className="Card"
                // onClick={()=>{navigate('/class')}}
                // onClick={() => {
                //   //   setSelectedNews(data);
                //   setSelectedLecture(data);
                //   console.log(data);
                //   navigate(`/class/${data.id}`);
                //   // console.log(data);
                // }}
              >
                <CardContent>
                    <Box sx={{display:'flex',flexDirection:'column',justifyContent:'center',alignItems:'center'}}>
                    <Box >
                    <Typography
                      gutterBottom
                      variant="h5"
                      component="div"
                      style={txtStyle}
                      sx={{ fontWeight: 450 }}
                      className="Heading"
                    >
                      Shreya Shah
                      {/* {data.subject.name} */}
                    </Typography>
                  </Box>
                  
                  <Box
                    sx={{
                      display: "flex",
                      flexDirection: "row",
                      marginBottom: "2px",
                    }}
                    className="Detail"
                  >
                   
                    <Typography
                      variant="body2"
                      color="white"
                      fontSize={"17px"}
                    >
                      Mumbai
                    </Typography>
                  </Box>
                    </Box>
                  
                  
                </CardContent>
                <CardActions sx={{ float: "right" }}>
                <Button
                    size="40rem"
                    sx={{color:'white'}}
                    
                  >
                    <ModeEditIcon color='white' fontSize='large'/>
                  </Button>
                <Button
                    size="40rem"
                    sx={{color:'white'}}
                    // onClick={() => {
                    //   //   setSelectedNews(data);
                    //   setSelectedLecture(data);
                    //   localStorage.setItem(
                    //     "LectureLocalStorage",
                    //     JSON.stringify(data)
                    //   );
                    //   navigate(`/class/${data.id}`);
                    //   // localStorage.setItem("classId", data.id);
                    //   // console.log(data);
                    // }}
                  >
                    <DeleteIcon color='white' fontSize='large'/>
                  </Button>
                </CardActions>
              </Card>

        </Box>
        </Box>
        


    </Box>
    
  )
}

export default Profile
