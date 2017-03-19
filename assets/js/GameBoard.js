import React from 'react';
import Cell from './Cell';
import $ from 'jquery';

const CLICK = 0;
const DOUBLE_CLICK = 1;
const FLAG = 2;

const GameBoard = (props) => {
    const {gameState, win, lost, setGameState, gameId, minesLeft} = props;
    const sendAction = (action_type, x, y) => {
        if (window.socket) {
            window.socket.send(window.gameClientId);
        }
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
                minesLeft: data.minesLeft,
            });
        })
        .catch((err) => {console.log(err)});
    };
    const undo = () => {
        if (window.socket) {
            window.socket.send(window.gameClientId);
        }
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
                minesLeft: data.minesLeft,
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
                                boomed={item === true}
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
                <div
                    className="notification notification__success"
                >
                    You Win
                </div>
            )
        }
        if (lost) {
            return (
                <div
                    className="notification notification__fail"
                >
                    You Lost
                </div>
            )
        }
        return (
            <div
                className="notification"
            >
                Django Mine Sweeper
            </div>
        );
    })();
    return(
        <div>
            {notification}
            <div className="stats">
                Mines Left: {minesLeft}
            </div>
            <div
                className="game-board"
            >
                {rows}
            </div>
            <div className="actions">
                <a className="button" onClick={undo}>Undo</a>
            </div>
            <div className="actions">
                <a
                    className="button"
                    onClick={() => {
                        setGameState({
                            gameId: 0,
                            gameState: [],
                            win: false,
                            lost: false,
                            minesLeft: 0,
                        });
                        window.history.replaceState('page', 'title', '/')
                    }}
                >New Game</a>
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