import React from 'react';
import Cell from './Cell';
import $ from 'jquery';

const CLICK = 0;
const DOUBLE_CLICK = 1;
const FLAG = 2;

const GameBoard = (props) => {
    const {gameState, win, lost, setGameState, gameId} = props;
    const sendAction = (action_type, x, y) => {
        $.ajax({
            method: 'POST',
            url: `/api/game/${gameId}/action/`,
            data: JSON.stringify({
                action_type,
                x,
                y,
            }),
            dataType: 'json',
            contentType: "application/json",
        })
        .done((data) => {
            setGameState({
                win: data.win,
                lost: data.lost,
                gameState: data.state,
            });
        })
        .catch((err) => {console.log(err)});
    };
    const undo = () => {
        $.ajax({
            method: 'get',
            url: `/api/game/${gameId}/back/`,
            contentType: "application/json",
        })
        .done((data) => {
            setGameState({
                win: data.win,
                lost: data.lost,
                gameState: data.state,
            });
        })
        .catch((err) => {console.log(err)});
    };
    const onClickLocation = (x, y) => (e) => {
        e.preventDefault();
        const which = e.nativeEvent.which;
        if (which === 1) {
            return sendAction(CLICK, x, y)
        }
        if (which === 3) {
            return sendAction(FLAG, x, y)
        }
    };
    const onDoubleClickLocation = (x, y) => (e) => {
        e.preventDefault();
        return sendAction(DOUBLE_CLICK, x, y)
    };
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
                        return (
                            <Cell
                                onRightClick={onClickLocation(x, y)}
                                onClick={onClickLocation(x, y)}
                                onDoubleClick={onDoubleClickLocation(x, y)}
                                key={location}
                                value={item}
                                location={[x, y]}
                            />
                        )
                    })
                }
            </div>
        )
    });
    const notification = (() => {
        if (win) {
            return (
                <span className="success">You win</span>
            )
        }
        if (lost) {
            return (
                <span className="success">You Lost</span>
            )
        }
        return null;
    })();
    return(
        <div>
            <div className="notification">
                {notification}
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
                <a className="button" onClick={undo}>Undo</a>
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