import React from 'react';

import styles from './Nav.css'
import { NavLink } from 'react-router-dom';
import UserService from '../../../services/UserService';

const links = [
    {
        title: "Register",
        destination: "/register",
    },
    {
        title: "Login",
        destination: "/login",
    },
    {
        title: "Home",
        destination: "/home",
    }
]

export default function Nav({isLoggedIn}) {

    const logout = () => {
        UserService.logOut()
    }

    const linkElements = 
        links.filter(link => {
            // Remove "Register" and "Login" when logged in
            return !isLoggedIn || !(link.title === "Register" || link.title === "Login")
        })
        .map(
            (link, index) =>
                <li key={index}>
                    <NavLink to={link.destination} activeClassName={styles.active}>
                        {link.title}
                    </NavLink>
                </li>
        )

    return (
        <div className="container">
            <nav>
                <ul>
                    {linkElements}
                </ul>
                {isLoggedIn && <button onClick={logout}>Log Out</button>}
            </nav>
        </div>
    )
};