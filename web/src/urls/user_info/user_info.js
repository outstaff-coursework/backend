import React from "react";
import Header from '../../components/header/header';
import Footer from '../../components/footer/footer';
import './user_info.css';

class UserInfo extends React.Component {
    constructor(props) {
        super(props)

        this.state = {}
        this.state.example_info_table = {
            'Дата рождения': '26 июня 2003 года',
            'Дата выхода на работу': '7 июля 2023 года',
        }
        this.state.example_contacts_table = {
            'Telegram': '@address',
            'Phone': '+7 800 555 35 35',
            'E-mail': 'adress@example.com',
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

    render() {
        return (
            <>
                <Header />
                <div className='page'>
                    <div className='page-info'>
                        <div className='page-info-photo' />
                        <div className='page-info-data'>
                            <div className='page-info-data-name'>
                                <h4>Иван Иванов</h4>
                            </div>
                            <div className='page-info-data-post'>
                                <span className='minor-text'>Разработчик</span>
                            </div>
                            <div className='page-info-data-status'>
                                <h6 className='contrast-text'>На встрече с 11:00 до 12:00</h6>
                            </div>
                            <div className='page-info-data-full_post'>
                                <span>Компания | Департамент | Служба | Отдел | Команда | Ещё что-нибудь</span>
                            </div>
                            <div className='page-info-data-about'>
                                <h6>О себе:</h6>
                                <span>Какая-то информация о себе или предложения о том, с кем можно было бы связаться, когда связаться с данным пользователем невозможно.</span>
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
                                    {this.genTable(this.state.example_contacts_table)}
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
