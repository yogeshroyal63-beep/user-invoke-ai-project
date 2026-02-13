import React from "react";

export default class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    console.error("UI Crash:", error, info);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="h-screen flex items-center justify-center bg-black text-white">
          <div className="text-center space-y-3">
            <h1 className="text-2xl font-bold">Something went wrong</h1>
            <p className="text-slate-400">
              Please refresh the page.
            </p>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}
