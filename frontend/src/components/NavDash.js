import { Navbar } from 'flowbite-react'
import { NavbarBrand } from 'flowbite-react/lib/esm/components/Navbar/NavbarBrand'
// import '../pages/Home/Home.css'
import { NavbarLink } from 'flowbite-react/lib/esm/components/Navbar/NavbarLink'
import { Button } from 'flowbite-react'
import { NavbarCollapse } from 'flowbite-react/lib/esm/components/Navbar/NavbarCollapse'
import { NavbarToggle } from 'flowbite-react/lib/esm/components/Navbar/NavbarToggle'

// import '../styles/Home.css'
// import x from '../Images/icon.png'
import { useNavigate } from 'react-router-dom'
import { useState } from 'react'
import './Nav.css'

import SettingsIcon from '@mui/icons-material/Settings';
import { Link } from 'react-router-dom'
import React from 'react'

const NavDash = () => {
  // navigate = useNavigate()

  // const handleSettingsClicks = () =>
  // {
  //   navigate('/settings')
  // }
 
    return (
        <Navbar
        // fluid
        // rounded
        fixed
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
          
          {/* <NavbarToggle /> */}
        </div>
        <Button  className='dash-button' as={Link} to='/profile'>
           <SettingsIcon color='white'/>
          </Button>
      </Navbar>
      )
  
}

export default NavDash
