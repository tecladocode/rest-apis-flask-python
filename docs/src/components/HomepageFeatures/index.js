import React from "react";
import clsx from "clsx";
import styles from "./styles.module.css";

const FeatureList = [
  {
    title: "Everything you need",
    Svg: require("@site/static/img/product-dev.svg").default,
    description: (
      <>
        Learn Flask, Docker, PostgreSQL, and more. Build professional-grade REST
        APIs with Python.
      </>
    ),
  },
  {
    title: "The latest versions",
    Svg: require("@site/static/img/cloud-download.svg").default,
    description: (
      <>
        No more outdated tutorials. Use Python 3.10+ and the latest versions of
        every Flask extension and library.
      </>
    ),
  },
  {
    title: "Use best practices",
    Svg: require("@site/static/img/robot-coding.svg").default,
    description: (
      <>
        Run your apps in Docker, host your code with Git, write documentation
        with Swagger, and test your APIs while developing.
      </>
    ),
  },
];

function Feature({ Svg, title, description }) {
  return (
    <div className={clsx("col col--4")}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
