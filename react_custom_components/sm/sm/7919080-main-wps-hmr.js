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


/**
 * ExampleComponent is an example component.
 * It takes a property, `label`, and
 * displays it.
 * It renders an input with the property `value`
 * which is editable by the user.
 */

function SideMenu(_ref) {
  var items = _ref.items;
  return /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement("nav", null, /*#__PURE__*/react__WEBPACK_IMPORTED_MODULE_0___default.a.createElement(Scrollspy, {
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
   * A label that will be printed when this component is rendered.
   */
  label: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string.isRequired,

  /**
   * The value displayed in the input.
   */
  value: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.string,

  /**
   * Dash-assigned callback that should be called to report property changes
   * to Dash, to make them available for callbacks.
   */
  setProps: prop_types__WEBPACK_IMPORTED_MODULE_1___default.a.func
};

/***/ })

})
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly9zbS8uL3NyYy9saWIvY29tcG9uZW50cy9TaWRlTWVudS5yZWFjdC5qcyJdLCJuYW1lcyI6WyJTaWRlTWVudSIsIml0ZW1zIiwibWFwIiwiaWQiLCJsYWJlbCIsImRlZmF1bHRQcm9wcyIsInByb3BUeXBlcyIsIlByb3BUeXBlcyIsInN0cmluZyIsImlzUmVxdWlyZWQiLCJ2YWx1ZSIsInNldFByb3BzIiwiZnVuYyJdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQUE7QUFBQTtBQUFBO0FBQ0E7QUFFQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUFDZSxTQUFTQSxRQUFULE9BQTZCO0FBQUEsTUFBVEMsS0FBUyxRQUFUQSxLQUFTO0FBQzFDLHNCQUNFLHFGQUNFLDJEQUFDLFNBQUQ7QUFBVyxTQUFLLEVBQUVBLEtBQUssQ0FBQ0MsR0FBTixDQUFVO0FBQUEsVUFBR0MsRUFBSCxTQUFHQSxFQUFIO0FBQUEsYUFBWUEsRUFBWjtBQUFBLEtBQVYsQ0FBbEI7QUFBNkMsb0JBQWdCLEVBQUM7QUFBOUQsS0FDR0YsS0FBSyxDQUFDQyxHQUFOLENBQVU7QUFBQSxRQUFHQyxFQUFILFNBQUdBLEVBQUg7QUFBQSxRQUFPQyxLQUFQLFNBQU9BLEtBQVA7QUFBQSx3QkFDVCxvRkFDRTtBQUFHLFVBQUksYUFBTUQsRUFBTixDQUFQO0FBQW1CLFNBQUcsRUFBRUE7QUFBeEIsT0FDR0MsS0FESCxDQURGLENBRFM7QUFBQSxHQUFWLENBREgsQ0FERixDQURGO0FBYUQ7QUFFREosUUFBUSxDQUFDSyxZQUFULEdBQXdCLEVBQXhCO0FBRUFMLFFBQVEsQ0FBQ00sU0FBVCxHQUFxQjtBQUNqQjtBQUNKO0FBQ0E7QUFDSUgsSUFBRSxFQUFFSSxpREFBUyxDQUFDQyxNQUpHOztBQU1qQjtBQUNKO0FBQ0E7QUFDSUosT0FBSyxFQUFFRyxpREFBUyxDQUFDQyxNQUFWLENBQWlCQyxVQVRQOztBQVdqQjtBQUNKO0FBQ0E7QUFDSUMsT0FBSyxFQUFFSCxpREFBUyxDQUFDQyxNQWRBOztBQWdCakI7QUFDSjtBQUNBO0FBQ0E7QUFDSUcsVUFBUSxFQUFFSixpREFBUyxDQUFDSztBQXBCSCxDQUFyQixDIiwiZmlsZSI6Ijc5MTkwODAtbWFpbi13cHMtaG1yLmpzIiwic291cmNlc0NvbnRlbnQiOlsiaW1wb3J0IFJlYWN0LCB7Q29tcG9uZW50fSBmcm9tICdyZWFjdCc7XG5pbXBvcnQgUHJvcFR5cGVzIGZyb20gJ3Byb3AtdHlwZXMnO1xuXG4vKipcbiAqIEV4YW1wbGVDb21wb25lbnQgaXMgYW4gZXhhbXBsZSBjb21wb25lbnQuXG4gKiBJdCB0YWtlcyBhIHByb3BlcnR5LCBgbGFiZWxgLCBhbmRcbiAqIGRpc3BsYXlzIGl0LlxuICogSXQgcmVuZGVycyBhbiBpbnB1dCB3aXRoIHRoZSBwcm9wZXJ0eSBgdmFsdWVgXG4gKiB3aGljaCBpcyBlZGl0YWJsZSBieSB0aGUgdXNlci5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgZnVuY3Rpb24gU2lkZU1lbnUoeyBpdGVtcyB9KSB7XG4gIHJldHVybiAoXG4gICAgPG5hdj5cbiAgICAgIDxTY3JvbGxzcHkgaXRlbXM9e2l0ZW1zLm1hcCgoeyBpZCB9KSA9PiBpZCl9IGN1cnJlbnRDbGFzc05hbWU9XCJzZWxlY3RlZFwiPlxuICAgICAgICB7aXRlbXMubWFwKCh7IGlkLCBsYWJlbCB9KSA9PiAoXG4gICAgICAgICAgPGxpPlxuICAgICAgICAgICAgPGEgaHJlZj17YCMke2lkfWB9IGtleT17aWR9PlxuICAgICAgICAgICAgICB7bGFiZWx9XG4gICAgICAgICAgICA8L2E+XG4gICAgICAgICAgPC9saT5cbiAgICAgICAgKSl9XG4gICAgICA8L1Njcm9sbHNweT5cbiAgICA8L25hdj5cbiAgKTtcbn1cblxuU2lkZU1lbnUuZGVmYXVsdFByb3BzID0ge307XG5cblNpZGVNZW51LnByb3BUeXBlcyA9IHtcbiAgICAvKipcbiAgICAgKiBUaGUgSUQgdXNlZCB0byBpZGVudGlmeSB0aGlzIGNvbXBvbmVudCBpbiBEYXNoIGNhbGxiYWNrcy5cbiAgICAgKi9cbiAgICBpZDogUHJvcFR5cGVzLnN0cmluZyxcblxuICAgIC8qKlxuICAgICAqIEEgbGFiZWwgdGhhdCB3aWxsIGJlIHByaW50ZWQgd2hlbiB0aGlzIGNvbXBvbmVudCBpcyByZW5kZXJlZC5cbiAgICAgKi9cbiAgICBsYWJlbDogUHJvcFR5cGVzLnN0cmluZy5pc1JlcXVpcmVkLFxuXG4gICAgLyoqXG4gICAgICogVGhlIHZhbHVlIGRpc3BsYXllZCBpbiB0aGUgaW5wdXQuXG4gICAgICovXG4gICAgdmFsdWU6IFByb3BUeXBlcy5zdHJpbmcsXG5cbiAgICAvKipcbiAgICAgKiBEYXNoLWFzc2lnbmVkIGNhbGxiYWNrIHRoYXQgc2hvdWxkIGJlIGNhbGxlZCB0byByZXBvcnQgcHJvcGVydHkgY2hhbmdlc1xuICAgICAqIHRvIERhc2gsIHRvIG1ha2UgdGhlbSBhdmFpbGFibGUgZm9yIGNhbGxiYWNrcy5cbiAgICAgKi9cbiAgICBzZXRQcm9wczogUHJvcFR5cGVzLmZ1bmNcbn07XG4iXSwic291cmNlUm9vdCI6IiJ9