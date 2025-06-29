import React from "react";
import { render, fireEvent, screen, waitFor } from "@testing-library/react";
import App from "./App";
import axios from "axios";

jest.mock("axios");

test("logs in and shows content generator", async () => {
  axios.post.mockResolvedValueOnce({
    data: { access_token: "dummy-token" }
  });

  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), {
    target: { value: "alice" }
  });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), {
    target: { value: "secret" }
  });
  fireEvent.click(screen.getByText("Login"));
  await waitFor(() =>
    expect(screen.getByText(/Content Generator/i)).toBeInTheDocument()
  );
});

test("generates content and displays it", async () => {
  axios.post.mockResolvedValueOnce({ data: { access_token: "dummy-token" } });
  axios.post.mockResolvedValueOnce({
    data: { content: "Welcome to our platform!", variant: "A" }
  });

  render(<App />);
  // Log in
  fireEvent.change(screen.getByPlaceholderText(/Username/i), {
    target: { value: "alice" }
  });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), {
    target: { value: "secret" }
  });
  fireEvent.click(screen.getByText("Login"));
  await waitFor(() => screen.getByText(/Content Generator/i));

  // Generate content
  fireEvent.change(screen.getByRole("textbox"), {
    target: { value: "Write a welcome message" }
  });
  fireEvent.click(screen.getByText("Generate"));

  await waitFor(() =>
    expect(screen.getByText("Welcome to our platform!")).toBeInTheDocument()
  );
  await waitFor(() =>
    expect(screen.getByText(/Variant: A/)).toBeInTheDocument()
  );
});

test("user submits thumbs up feedback", async () => {
  axios.post.mockResolvedValueOnce({ data: { access_token: "dummy-token" } }); // login
  axios.post.mockResolvedValueOnce({ data: { content: "Text", variant: "B" } }); // generate
  axios.post.mockResolvedValueOnce({}); // feedback

  render(<App />);
  fireEvent.change(screen.getByPlaceholderText(/Username/i), { target: { value: "alice" } });
  fireEvent.change(screen.getByPlaceholderText(/Password/i), { target: { value: "secret" } });
  fireEvent.click(screen.getByText("Login"));
  await waitFor(() => screen.getByText(/Content Generator/i));
  fireEvent.change(screen.getByRole("textbox"), { target: { value: "Prompt" } });
  fireEvent.click(screen.getByText("Generate"));
  await waitFor(() => screen.getByText("Text"));
  fireEvent.click(screen.getByText("👍"));
  await waitFor(() => screen.getByText(/thanks for your feedback/i));
});