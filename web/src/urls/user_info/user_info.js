import React from "react";
import Header from '../../components/header/header';
import Footer from '../../components/footer/footer';
import './user_info.css';
import {base_url} from "../../constants";

import axios from "axios";

class UserInfo extends React.Component {
    constructor(props) {
        super(props)

        this.state = {
            id: '-1',
            loaded_info: false,
            name: '...',
            nickname: '...',
            about_user: '...',
            photo_url: '...',
            position: '...',
        }
        this.state.example_info_table = {
            'Дата рождения': '26 июня 2003 года',
            'Дата выхода на работу': '7 июля 2023 года',
        }
        this.state.contacts_table = {
            'Telegram': '...',
            'Phone': '...',
            'E-mail': '...',
        }
        this.state.meetings = {
            today: {
                date: '09.11',
                meetings_list: [{
                        start: '11',
                        end: '12',
                    }, {
                        start: '13',
                        end: '16',
                    },
                ],
            },
            tomorrow: {
                date: '10.11',
                meetings_list: [{
                        start: '11',
                        end: '12',
                    }, {
                        start: '13',
                        end: '16',
                    },
                ],
            },
        }
    }

    genTable(data) {
        let table = []
        for (let key in data) {
            table.push(
                <div className='table-row'>
                    <span>{key}</span>
                    <span className='minor-text'>{data[key]}</span>
                </div>
            )
        }
        return table
    }

    genCalendarDataSpace(meetings_list) {
        let result = []
        for (let i = 0; i < 23; ++i) {
            result.push(
                <div className='page-calendar-data-space-line'></div>
            )
        }
        meetings_list.forEach(meeting => {
            let delta = (800 - 151) / 24 + 1
            let start_pos = Number(meeting.start) * delta
            let width = (Number(meeting.end) - Number(meeting.start)) * delta
            result.push(
                <div
                    className='page-calendar-data-space-meeting'
                    style={{left: start_pos.toString() + 'px', width: width.toString() + 'px'}}
                ></div>
            )
        }); 
        return result;
    }

    genCalendarData(is_today) {
        let result = []
        let meetings, panel_label
        if (is_today) {
            meetings = this.state.meetings.today
            panel_label = 'Сегодня'
        } else {
            meetings = this.state.meetings.tomorrow
            panel_label = 'Завтра'
        }
        let date = meetings.date
        let meetings_list = meetings.meetings_list
        result.push(
            <div className='page-calendar-data-panel'>
                <h6>{panel_label}</h6>
                <h6>{date}</h6>
            </div>
        )
        result.push(
            <div className='page-calendar-data-space'>
                {this.genCalendarDataSpace(meetings_list)}
            </div>
        )
        return result;
    }

    loadInfo() {
        if (this.state.id == '-1') {
            return
        }
        let url = base_url + '/user/' + this.state.id;
        axios.get(url).then(res => {
            let data = res.data;
            this.setState({
                contacts_table: {
                    'Telegram': data['telegram'],
                    'Phone': data['phone_number'],
                    'E-mail': data['email'],
                }
            })
            this.setState({
                loaded_info: true,
                name: data['name'],
                nickname: data['nickname'],
                about_user: data['user_about'],
                photo_url: data['photo_url'],
                position: data['position'],
            });
        });
    }

    componentDidUpdate(prevProps, prevState, snapshot) {
        if (prevState.id !== this.state.id) {
            this.loadInfo();
        }
    }

    componentDidMount() {
        let path = window.location.pathname;
        for (let i = path.length - 1; i > -1; --i) {
            if (path[i] === '/') {
                this.setState({id: path.slice(i + 1, path.length)});
                break;
            }
        }
    }

    render() {
        return (
            <>
                <Header />
                <div className='page'>
                    <div className='page-info'>
                        <div className='page-info-photo'>
                            <img src={this.state.photo_url} alt="photo" />
                        </div>
                        <div className='page-info-data'>
                            <div className='page-info-data-name'>
                                <h4>{this.state.name}</h4>
                            </div>
                            <div className='page-info-data-post'>
                                <span className='minor-text'>{this.state.position}</span>
                            </div>
                            <div className='page-info-data-status'>
                                <h6 className='contrast-text'>На встрече с 11:00 до 12:00</h6>
                            </div>
                            <div className='page-info-data-full_post'>
                                <span>Компания | Департамент | Служба | Отдел | Команда | Ещё что-нибудь</span>
                            </div>
                            <div className='page-info-data-about'>
                                <h6>О себе:</h6>
                                <span>{this.state.about_user}</span>
                            </div>
                            <div className='page-info-data-information'>
                                <h6>Информация:</h6>
                                <div className='table'>
                                    {this.genTable(this.state.example_info_table)}
                                </div>
                            </div>
                            <div className='page-info-data-contacts'>
                                <h6>Контакты:</h6>
                                <div className='table'>
                                    {this.genTable(this.state.contacts_table)}
                                </div>
                            </div>
                        </div>
                    </div>
                    <div className='page-calendar'>
                        <h6>Календарь на ближайшие дни:</h6>
                        <div className='page-calendar-data'>
                            {this.genCalendarData(true)}
                        </div>
                        <div className='page-calendar-data'>
                            {this.genCalendarData(false)}
                        </div>
                        <button className="page-calendar-button">Перейти в календарь</button>
                    </div>
                </div>
                <Footer />
            </>
        );
    }
}

export default UserInfo;
