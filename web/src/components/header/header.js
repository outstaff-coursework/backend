import React from "react";
import './header.css';

class Header extends React.Component {
    render() {
        return (
            <div className='header'>
                <div className='header-content'>
                    <div className='header-content-left'>
                        <div className='header-content-left-logo-section'>
                            <div className='header-content-left-logo-section-logo' />
                            <h5 className='header-content-left-logo-section-name'>Outstaff</h5>
                        </div>
                    </div>
                    <div className='header-content-right' />
                </div>
            </div>
        );
    }
}

export default Header;
