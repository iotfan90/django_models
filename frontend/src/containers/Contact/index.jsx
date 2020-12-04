import React, {Component} from "react"
import {connect} from 'react-redux'
import Card from "../../components/Card/Card.jsx"
import {getUserInfo} from '../../redux/actions/auth'
// import {Redirect} from "react-router";

class ContactUs extends Component{
  constructor(props) {
    super(props);
    this.state = {
      phoneNumber: this.props.user.phone_number,
    };
  }
  render() {
    return (
      <div>
        <Card
         content={
           <div style={{paddingLeft: 50}}>
             <p>You can contact support through email or phone below.</p>
             <p>Our phone is: 123456789‬</p>
             <p>Our email is: info@citybestrenovations.com</p>
           </div>
         }
        />
      </div>
    );
  }
}
const mapStateToProps = state => ({
  user: state.auth.user
});

const mapDispatchToProps = {
  getUserInfo,
};

export default connect(mapStateToProps, mapDispatchToProps)(ContactUs);
