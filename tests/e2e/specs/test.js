// https://docs.cypress.io/api/introduction/api.html

describe("Test main page", () => {
  it("Visits the app root url", () => {
    cy.visit("/");
    cy.contains("div", "CityRoute");
  });
});
