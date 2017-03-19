import React from 'react';
import $ from 'jquery';
import GameBoard from './GameBoard';
import { guid } from './utils';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gameState: [],
            gameId: 0,
            win: false,
            lost: false,
            minesLeft: 0,
            numOfMines: '10',
            x: '10',
            y: '10',
        };
        this.setGameState = (newState) => {
            this.setState(newState)
        };
        this.syncGameInfo = (gameId) => {
            gameId = gameId || this.state.gameId;
            $.ajax({
                method: 'GET',
                url: `/api/game/${gameId}`,
                dataType: 'json',
            })
            .done((data) => {
                this.setState({
                    win: data.win,
                    lost: data.lost,
                    gameState: data.state,
                    gameId: gameId,
                    minesLeft: data.minesLeft,
                });
            })
            .catch((err) => {console.log(err)});
        };
        this.newGame = () => {
            const { numOfMines, x, y} = this.state;
            $.ajax({
                method: 'POST',
                url: '/api/create/',
                data: JSON.stringify({
                    numOfMines: parseInt(numOfMines, 10),
                    size: [parseInt(x, 10), parseInt(y, 10)],
                }),
                dataType: 'json',
                contentType: "application/json",
            })
            .done((data) => {
                // console.log(data)
                this.setState({
                    gameState: data.state,
                    gameId: data.gameId,
                    minesLeft: data.minesLeft,
                });
                window.history.pushState('page', 'title', `/game/${data.gameId}`);
            })
            .catch((err) => {console.log(err)});
        };
        this.connectGameChannel = (gameId) => {
            if (WebSocket) {
                window.gameClientId = guid();
                window.socket = new WebSocket("ws://" + window.location.host + "/" + gameId +"/");
                socket.onmessage = (e) => {
                    if (e.data !== window.gameClientId) {
                        this.syncGameInfo();
                    }
                };
            }
        };
    }

    componentWillUpdate(nextProps, nextState) {
        if (nextState.gameId && nextState.gameId !== this.state.gameId) {
            return this.connectGameChannel(nextState.gameId);
        }
    }

    componentDidMount() {
        const initialId = window.initialGameId;
        if (initialId) {
            this.syncGameInfo(initialId);
        }
    }

    render() {
        if (this.state.gameState.length === 0) {
            return (
                <div className="app-container">
                    <div className="input-group">
                        <span className="input-label">Number Of Mines:</span>
                        <input
                            type="text"
                            value={this.state.numOfMines}
                            onChange={(e) => {
                                this.setState({numOfMines: e.target.value})
                            }}
                        />
                    </div>
                    <div className="input-group">
                        <span className="input-label">Number Of Rows:</span>
                        <input
                            type="text"
                            value={this.state.x}
                            onChange={(e) => {
                                this.setState({x: e.target.value})
                            }}
                        />
                    </div>
                    <div className="input-group">
                        <span className="input-label">Number Of Columns:</span>
                        <input
                            type="text"
                            value={this.state.y}
                            onChange={(e) => {
                                this.setState({y: e.target.value})
                            }}
                        />
                    </div>
                    <br/>
                    <div>
                        <a className="button button__start" onClick={this.newGame}>Start</a>
                    </div>
                </div>
            )
        }
        return (
            <div className="app-container">
                <GameBoard
                    setGameState={this.setGameState}
                    {...this.state}
                />
            </div>
        )
    }
}

export default App;