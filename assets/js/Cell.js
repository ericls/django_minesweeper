import React from 'react';

const Cell = (props) => {
    const {location, value} = props;
    const getColor = (value) => {
      switch (value) {
          case 1:
              return "#3b9f3b";
          case 2:
              return "#1f2d7b";
          case 3:
              return "#ff354b";
          case 4:
              return "#640004";
          case 5:
              return "#000aff";
          case 6:
              return "#ff00d3";
          case 7:
              return "#02470d";
          case 8:
              return "#585000";
          case 9:
              return "#5Aff5A";
      }
    };
    const getDisplayValue = (value) => {
      if (value === 9) {
          return <span>&#x1F6A9;</span>
      }
      if (value === 0) {
          return <span />
      }
      return <span style={{color: getColor(value)}}>{value}</span>
    };
    const getStyle = (value) => {
        if (value === null || value === 9) {
            return {
                backgroundColor: "#888",
            }
        }
        return {}
    };
    return (
        <div
            onClick={value ? () => {} : props.onClick}
            onDoubleClick={value ? props.onDoubleClick : () => {}}
            className="cell"
            style={getStyle(value)}
            onContextMenu={props.onRightClick}
        >
            {getDisplayValue(value)}
        </div>
    )
};

Cell.propTypes = {
    location: React.PropTypes.array.isRequired,
    value: React.PropTypes.number,
    onClick: React.PropTypes.func,
    onRightClick: React.PropTypes.func,
    onDoubleClick: React.PropTypes.func,
};

Cell.defaultProps = {
    value: 0,
    onClick: () => {},
    onDoubleClick: () => {},
    onRightClick: () => {},
};

export default Cell;