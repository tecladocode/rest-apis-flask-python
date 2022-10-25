import React from "react";
import clsx from "clsx";
import Layout from "@theme/Layout";
import Link from "@docusaurus/Link";
import useDocusaurusContext from "@docusaurus/useDocusaurusContext";
import styles from "./index.module.css";
import HomepageFeatures from "@site/src/components/HomepageFeatures";
import VideoEmbed from "@site/src/components/VideoEmbed";

function HomepageHeader() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <header className={clsx("hero hero--primary", styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs/course_intro/"
          >
            Read the e-book
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const { siteConfig } = useDocusaurusContext();
  return (
    <Layout
      title={`${siteConfig.title} e-book`}
      description="The full course notes and code"
    >
      <HomepageHeader />
      <main>
        <div
          style={{
            border: "4px solid black",
            maxWidth: "800px",
            margin: "4rem auto 4rem auto",
            boxShadow: "0 5px 15px 0 rgba(0, 0, 0, 0.15)",
          }}
        >
          <VideoEmbed url="https://customer-zmitazl0ztnd2pvm.cloudflarestream.com/1c4db6119cf0c6e682a88a737af146eb/iframe?poster=https%3A%2F%2Fcustomer-zmitazl0ztnd2pvm.cloudflarestream.com%2F1c4db6119cf0c6e682a88a737af146eb%2Fthumbnails%2Fthumbnail.jpg%3Ftime%3D%26height%3D600" />
        </div>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}
