webpackHotUpdatesm("main",{

/***/ "./src/lib/components/SideMenu.react.js":
/*!**********************************************!*\
  !*** ./src/lib/components/SideMenu.react.js ***!
  \**********************************************/
/*! exports provided: default */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "default", function() { return SideMenu; });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "./node_modules/react/index.js");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! prop-types */ "./node_modules/prop-types/index.js");
/* harmony import */ var prop_types__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(prop_types__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_scrollspy__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-scrollspy */ "./node_modules/react-scrollspy/lib/scrollspy.js");
/* harmony import */ var react_scrollspy__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_scrollspy__WEBPACK_IMPORTED_MODULE_2__);



/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */

function SideMenu(_ref) {
  var items = _ref.items,
      className = _ref.className;
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("nav", {
    className: className
  }, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(react_scrollspy__WEBPACK_IMPORTED_MODULE_2___default.a, {
    items: items.map(function (_ref2) {
      var id = _ref2.id;
      return id;
    }),
    currentClassName: "selected"
  }, items.map(function (_ref3) {
    var id = _ref3.id,
        label = _ref3.label;
    return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("li", null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("a", {
      href: "#".concat(id),
      key: id
    }, label));
  })));
}
SideMenu.defaultProps = {};
SideMenu.propTypes = {
  /**
   * The ID used to identify this component in Dash callbacks.
   */
  id: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * An array of id, label
   */
  items: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.array.isRequired,

  /**
   * Navbar class name
   */
  className: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string
};

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zbS8uL3NyYy9saWIvY29tcG9uZW50cy9TaWRlTWVudS5yZWFjdC5qcyJdLCJuYW1lcyI6WyJTaWRlTWVudSIsIml0ZW1zIiwiY2xhc3NOYW1lIiwibWFwIiwiaWQiLCJsYWJlbCIsImRlZmF1bHRQcm9wcyIsInByb3BUeXBlcyIsIlByb3BUeXBlcyIsInN0cmluZyIsImFycmF5IiwiaXNSZXF1aXJlZCJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUNBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFDZSxTQUFTQSxRQUFULE9BQXdDO0FBQUEsTUFBcEJDLEtBQW9CLFFBQXBCQSxLQUFvQjtBQUFBLE1BQWJDLFNBQWEsUUFBYkEsU0FBYTtBQUNyRCxzQkFDRTtBQUFLLGFBQVMsRUFBRUE7QUFBaEIsa0JBQ0UsMkRBQUMsc0RBQUQ7QUFBVyxTQUFLLEVBQUVELEtBQUssQ0FBQ0UsR0FBTixDQUFVO0FBQUEsVUFBR0MsRUFBSCxTQUFHQSxFQUFIO0FBQUEsYUFBWUEsRUFBWjtBQUFBLEtBQVYsQ0FBbEI7QUFBNkMsb0JBQWdCLEVBQUM7QUFBOUQsS0FDR0gsS0FBSyxDQUFDRSxHQUFOLENBQVU7QUFBQSxRQUFHQyxFQUFILFNBQUdBLEVBQUg7QUFBQSxRQUFPQyxLQUFQLFNBQU9BLEtBQVA7QUFBQSx3QkFDVCxvRkFDRTtBQUFHLFVBQUksYUFBTUQsRUFBTixDQUFQO0FBQW1CLFNBQUcsRUFBRUE7QUFBeEIsT0FDR0MsS0FESCxDQURGLENBRFM7QUFBQSxHQUFWLENBREgsQ0FERixDQURGO0FBYUQ7QUFFREwsUUFBUSxDQUFDTSxZQUFULEdBQXdCLEVBQXhCO0FBRUFOLFFBQVEsQ0FBQ08sU0FBVCxHQUFxQjtBQUNqQjtBQUNKO0FBQ0E7QUFDSUgsSUFBRSxFQUFFSSxpREFBUyxDQUFDQyxNQUpHOztBQU1qQjtBQUNKO0FBQ0E7QUFDSVIsT0FBSyxFQUFFTyxpREFBUyxDQUFDRSxLQUFWLENBQWdCQyxVQVROOztBQVdqQjtBQUNKO0FBQ0E7QUFDSVQsV0FBUyxFQUFFTSxpREFBUyxDQUFDQztBQWRKLENBQXJCLEMiLCJmaWxlIjoiNzU4ZGY2Zi1tYWluLXdwcy1obXIuanMiLCJzb3VyY2VzQ29udGVudCI6WyJpbXBvcnQgUmVhY3QsIHtDb21wb25lbnR9IGZyb20gJ3JlYWN0JztcbmltcG9ydCBQcm9wVHlwZXMgZnJvbSAncHJvcC10eXBlcyc7XG5pbXBvcnQgU2Nyb2xsc3B5IGZyb20gXCJyZWFjdC1zY3JvbGxzcHlcIjtcblxuLyoqXG4gKiBFeGFtcGxlQ29tcG9uZW50IGlzIGFuIGV4YW1wbGUgY29tcG9uZW50LlxuICogSXQgdGFrZXMgYSBwcm9wZXJ0eSwgYGxhYmVsYCwgYW5kXG4gKiBkaXNwbGF5cyBpdC5cbiAqIEl0IHJlbmRlcnMgYW4gaW5wdXQgd2l0aCB0aGUgcHJvcGVydHkgYHZhbHVlYFxuICogd2hpY2ggaXMgZWRpdGFibGUgYnkgdGhlIHVzZXIuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGZ1bmN0aW9uIFNpZGVNZW51KHsgaXRlbXMsIGNsYXNzTmFtZSB9KSB7XG4gIHJldHVybiAoXG4gICAgPG5hdiBjbGFzc05hbWU9e2NsYXNzTmFtZX0+XG4gICAgICA8U2Nyb2xsc3B5IGl0ZW1zPXtpdGVtcy5tYXAoKHsgaWQgfSkgPT4gaWQpfSBjdXJyZW50Q2xhc3NOYW1lPVwic2VsZWN0ZWRcIj5cbiAgICAgICAge2l0ZW1zLm1hcCgoeyBpZCwgbGFiZWwgfSkgPT4gKFxuICAgICAgICAgIDxsaT5cbiAgICAgICAgICAgIDxhIGhyZWY9e2AjJHtpZH1gfSBrZXk9e2lkfT5cbiAgICAgICAgICAgICAge2xhYmVsfVxuICAgICAgICAgICAgPC9hPlxuICAgICAgICAgIDwvbGk+XG4gICAgICAgICkpfVxuICAgICAgPC9TY3JvbGxzcHk+XG4gICAgPC9uYXY+XG4gICk7XG59XG5cblNpZGVNZW51LmRlZmF1bHRQcm9wcyA9IHt9O1xuXG5TaWRlTWVudS5wcm9wVHlwZXMgPSB7XG4gICAgLyoqXG4gICAgICogVGhlIElEIHVzZWQgdG8gaWRlbnRpZnkgdGhpcyBjb21wb25lbnQgaW4gRGFzaCBjYWxsYmFja3MuXG4gICAgICovXG4gICAgaWQ6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBBbiBhcnJheSBvZiBpZCwgbGFiZWxcbiAgICAgKi9cbiAgICBpdGVtczogUHJvcFR5cGVzLmFycmF5LmlzUmVxdWlyZWQsXG5cbiAgICAvKipcbiAgICAgKiBOYXZiYXIgY2xhc3MgbmFtZVxuICAgICAqL1xuICAgIGNsYXNzTmFtZTogUHJvcFR5cGVzLnN0cmluZ1xufTtcbiJdLCJzb3VyY2VSb290IjoiIn0=