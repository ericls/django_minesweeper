import React from 'react';
import GameBoard from './GameBoard';

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            gameState: [],
            win: false,
            lost: false,
            numOfMines: '10',
            x: '10',
            y: '10',
        };
        this.newGame = () => {
            this.setState({
                gameState: [
                    [0, 1, 1, 1, 0],
                    [0, 1, 9, 2, 1],
                    [1, 2, 2, null, null],
                    [null, null, null, null, null],
                    [null, null, null, null, null],
                ],
            })
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
                <GameBoard gameState={this.state.gameState} win={this.state.win} lost={this.state.lost} />
            </div>
        )
    }
}

export default App;