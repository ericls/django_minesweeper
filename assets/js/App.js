import React from 'react';
import $ from 'jquery';
import GameBoard from './GameBoard';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gameState: [],
            gameId: 0,
            win: false,
            lost: false,
            numOfMines: '10',
            x: '10',
            y: '10',
        };
        this.setGameState = (newState) => {
            this.setState(newState)
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
                });
                window.history.pushState('page', 'title', `/game/${data.gameId}`);
            })
            .catch((err) => {console.log(err)});
        }
    }

    componentDidMount() {
        const initialId = window.initialGameId;
        if (initialId) {
            $.ajax({
                method: 'GET',
                url: `/api/game/${initialId}`,
                dataType: 'json',
            })
            .done((data) => {
                this.setState({
                    win: data.win,
                    lost: data.lost,
                    gameState: data.state,
                    gameId: initialId,
                });
            })
            .catch((err) => {console.log(err)});
        }
    }

    render() {
        if (this.state.gameState.length === 0) {
            return (
                <div>
                    Number Of Mines:
                    <br/>
                    <input
                        type="text"
                        value={this.state.numOfMines}
                        onChange={(e) => {
                            this.setState({numOfMines: e.target.value})
                        }}
                    />
                    <br/>
                    Rows:
                    <br/>
                    <input
                        type="text"
                        value={this.state.x}
                        onChange={(e) => {
                            this.setState({x: e.target.value})
                        }}
                    />
                    <br/>
                    Cols:
                    <br/>
                    <input
                        type="text"
                        value={this.state.y}
                        onChange={(e) => {
                            this.setState({y: e.target.value})
                        }}
                    />
                    <br/>
                    <a className="button" onClick={this.newGame}>Start New Game</a>
                </div>
            )
        }
        return (
            <div>
                <GameBoard
                    setGameState={this.setGameState}
                    gameState={this.state.gameState}
                    win={this.state.win}
                    lost={this.state.lost}
                    gameId={this.state.gameId}
                />
            </div>
        )
    }
}

export default App;