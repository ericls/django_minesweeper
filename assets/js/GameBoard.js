import React from 'react';
import Cell from './Cell';

const GameBoard = (props) => {
    const {gameState, win, lost} = props;
    const rows = gameState.map((row, x) => {
        return (
            <div
                key={x}
                className="game-board-row"
                style={{
                    display: "flex",
                    flexDirection: "row",
                }}
            >
                {
                    row.map((item, y) => {
                        const location = [x, y];
                        return <Cell key={location}  value={item} location={[x, y]} />
                    })
                }
            </div>
        )
    });
    return(
        <div>
            <div className="notification">
            </div>
            <div className="stats">
            </div>
            <div
                className="game-board"
                style={{
                    display: "flex",
                    flexDirection: "column",
                    border: "solid 2px #999",
                }}
            >
                {rows}
            </div>
            <div className="actions">
                <a className="button" onClick={() => {}}>Regret</a>
            </div>
        </div>
    )
};

GameBoard.propTypes = {
    gameState: React.PropTypes.array,
    win: React.PropTypes.bool,
    lost: React.PropTypes.bool,
};

GameBoard.defaultProps = {
    gameState: [],
    win: false,
    lost: false,
};

export default GameBoard;