import { Navbar } from 'flowbite-react'
import { NavbarBrand } from 'flowbite-react/lib/esm/components/Navbar/NavbarBrand'
// import '../pages/Home/Home.css'
import { NavbarLink } from 'flowbite-react/lib/esm/components/Navbar/NavbarLink'
import { Button } from 'flowbite-react'
import { NavbarCollapse } from 'flowbite-react/lib/esm/components/Navbar/NavbarCollapse'
import { NavbarToggle } from 'flowbite-react/lib/esm/components/Navbar/NavbarToggle'

// import '../styles/Home.css'
// import x from '../Images/icon.png'
// import { useNavigate } from 'react-router-dom'
import { useState,useRef } from 'react'

// import GavelIcon from '@mui/icons-material/Gavel';
export default function Nav() {
//   const navigate = useNavigate();

  return (
    <Navbar
    fluid
    // rounded
    className='nav'
    
  >
    <NavbarBrand href="https://flowbite-react.com">
      {/* <img
        alt="logo"
        className="mr-3 h-6 sm:h-9"
        src={x}
      /> */}
      {/* <NavbarIcon> */}
     
   
      
      <span className="self-center whitespace-nowrap text-xl text-white font-semibold dark:text-white color-[white]">
        Aura      </span>
    </NavbarBrand>
    <div className="flex md:order-2">
      
      <NavbarToggle />
    </div>
    <NavbarCollapse className='nav-col lg: bg-black z-10 '  >
      <NavbarLink
        active
        href="#"
      >
        <p style={{
          color:'white',
          fontSize:'18px'
        }}>
          Home
        </p>
      </NavbarLink>
      <NavbarLink href="#"
      style={{
        color:'white',
        fontSize:'18px'
      }}>
        About us
      </NavbarLink>
      <NavbarLink href="#" style={{
          color:'white',
          fontSize:'18px'
        }}>
        Testimonials
      </NavbarLink>
      <NavbarLink href="#" style={{
          color:'white',
          fontSize:'18px'
        }}>
        Contact us
      </NavbarLink>
     
    </NavbarCollapse>
    <Button className='button'
      style={{
          width:100
      }} >
        Login
      </Button>
  </Navbar>
  )
}
