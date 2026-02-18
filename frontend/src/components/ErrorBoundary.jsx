import React from "react";

export default class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(err) {
    console.error("Component crashed:", err);
  }

  render() {
    if (this.state.hasError) {
      return <p className="error">Unable to render this section</p>;
    }
    return this.props.children;
  }
}
